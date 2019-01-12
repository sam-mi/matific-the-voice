

# ----------------------------------------------------------
#   TIMESTAMPED
# ----------------------------------------------------------
from django.db import models
from django.utils import timezone
from model_utils import Choices
from model_utils.models import StatusModel
from django.utils.translation import ugettext as _


class AbstractTimestampBase(models.Model):
    """
    Abstract base model with common fields and methods for all models.

    Add ``created`` and ``modified`` timestamp fields. Update the ``modified``
    field automatically on save. Sort by primary key.
    """

    created = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        editable=False
    )
    modified = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        editable=False
    )

    # TODO: Manager

    class Meta:
        abstract = True
        get_latest_by = 'pk'
        ordering = ('-id', )

    def save(self, *args, **kwargs):
        """
        Update ``self.modified``.
        """
        self.modified = timezone.now()
        super(AbstractTimestampBase, self).save(*args, **kwargs)


class AbstractTimestampedModel(AbstractTimestampBase):
    """
    Consistent naming
    """

    class Meta:
        abstract = True



# ----------------------------------------------------------
#   STATUS
# ----------------------------------------------------------

class AbstractStatusModel(StatusModel):

    ACTIVE = Choices(
        ('active', _('Active')),
    )

    CLOSED = Choices(
        ('closed', _('Closed')),
        ('inactive', _('Inactive')),
    )
    STATUS = Choices(*ACTIVE, *CLOSED)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'active' not in self.active_list():
            raise NotImplementedError(
                "'active' must be in property ACTIVE "
                "on class %s" % self.__class__.__name__
            )
        if 'inactive' not in self.closed_list():
            # or 'closed' not in self.CLOSED:
            raise NotImplementedError(
                "'inactive' or 'closed' must in in property CLOSED "
                "on class %s" % self.__class__.__name__
            )
        self.STATUS = Choices(*self.ACTIVE, *self.CLOSED)


    # TODO: Manager

    @classmethod
    def active_list(cls):
        return [s[0] for s in cls.ACTIVE]

    @classmethod
    def closed_list(cls):
        return [s[0] for s in cls.CLOSED]

    @property
    def is_active(self):
        return self.status in self.active_list()

    def check_closed(self):
        return self.status in self.closed_list()

    def check_in_active(self, string):
        return string in [s[0] for s in self.ACTIVE]

    def check_in_closed(self, string):
        return string in [s[0] for s in self.CLOSED]

    def set_status(self, value):
        '''
        Sets the status if a valid status or ignores

        :param value: a value in Option.STATUS choices or Bool
        :return: None
        '''
        if value == True:
            self.status = self.STATUS.active
        elif value == False:
            if 'inactive' in self.CLOSED:
                self.status = self.STATUS.inactive
            elif 'closed' in self.CLOSED:
                self.status = self.STATUS.closed
        if self.is_active:
            self.status = value
        else:
            return
        self.save()

    class Meta:
        abstract = True



# ----------------------------------------------------------
#   COMBINED
# ----------------------------------------------------------

class AbstractTimeStampedStatusModel(AbstractTimestampBase, AbstractStatusModel):
    """
    Convenience for TimeStamped and Status models combined.
    """
    # TODO: Combined Managers


    class Meta:
        abstract = True
