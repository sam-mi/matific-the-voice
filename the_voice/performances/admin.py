from django.contrib import admin
from django.contrib.postgres.forms import RangeWidget
from floppyforms import SplitDateTimeWidget

from the_voice.performances.models import Team, Song, Performance, Score


# @admin.register()
# class MentorInline(admin.StackedInline):




@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    list_display = [
        'title', 'status', 'created', 'modified'
    ]
    readonly_fields = [
        'created', 'modified'
    ]
    fields = [
        'created', 'modified', 'title', 'slug', 'status', 'mentors', 'candidates'
    ]
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('mentors', 'candidates',)

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
        '__str__', 'score', 'created', 'modified'
    ]
    readonly_fields = [
        'created', 'modified'
    ]
    fields = [
        'created', 'modified', 'mentor', 'performance', 'score'
    ]

    class Meta:
        fields = "__all__"



@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):

    list_display = [
        '__str__', 'status', 'created', 'modified'
    ]
    readonly_fields = [
        'created', 'modified'
    ]
    fields = [
        'created', 'modified', 'status', 'timeslot', 'performer', 'song'
    ]
    class Meta:
        fields = "__all__"
