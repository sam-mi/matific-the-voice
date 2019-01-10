from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.postgres.forms import RangeWidget
from floppyforms import SplitDateTimeWidget

from the_voice.performances.models import Team, Song, Performance, Score


# @admin.register()
# class MentorInline(admin.StackedInline):

User = get_user_model()

class CandidateInline(admin.TabularInline):

    model = User
    extra = 0

    fields = ('name', 'user_type')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    list_display = [
        'title', 'status', 'created', 'modified'
    ]
    readonly_fields = [
        'created', 'modified'
    ]
    fields = [
        'created', 'modified', 'title', 'slug', 'status', 'mentors',
    ]
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('mentors',)

    inlines = [CandidateInline]

    class Meta:
        fields = "__all__"



@admin.register(Song)
class SongAdmin(admin.ModelAdmin):

    list_display = [
        'title', 'created', 'modified'
    ]
    readonly_fields = [
        'created', 'modified'
    ]
    fields = [
        'created', 'modified', 'title',
    ]

    class Meta:
        fields = "__all__"



@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):

    list_display = [
        '__str__', 'score', 'performance', 'created', 'modified'
    ]
    readonly_fields = [
        'created', 'modified'
    ]
    fields = [
        'created', 'modified', 'mentor', 'performance', 'score'
    ]

    # TODO: modify the form to filter the mentor list by user_type=='mentor'

    class Meta:
        fields = "__all__"



@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):

    list_display = [
        '__str__', 'performer', 'song', 'team', 'timeslot', 'status', 'created', 'modified'
    ]
    readonly_fields = [
        'created', 'modified'
    ]
    fields = [
        'created', 'modified', 'status', 'timeslot', 'performer', 'song', 'team'
    ]
    class Meta:
        fields = "__all__"
