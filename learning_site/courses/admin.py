from datetime import date

from django.contrib import admin

from . import models


# Admin actions
def make_published(modeladmin, request, queryset):
    queryset.update(status='p', published=True)


make_published.short_description = "Mark selected courses as Published"


def make_in_review(modeladmin, request, queryset):
    queryset.update(status='r', published=False)


make_in_review.short_description = "Mark selected courses as In Review"


@admin.action(description="Mark selected courses as In Progress")  # from 3.2
def make_in_progress(modeladmin, request, queryset):
    queryset.update(status='i', published=False)


admin.site.disable_action('delete_selected')  # globally(site-level) disabled


# Inline Form
class TextInline(admin.StackedInline):
    model = models.Text
    fieldsets = (
        (None, {'fields': (('title', 'order'), 'description', 'content')}),
    )


class QuizInline(admin.StackedInline):
    model = models.Quiz


class AnswerInline(admin.TabularInline):
    model = models.Answer


# Filters
class YearListFilter(admin.SimpleListFilter):
    title = 'year created'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        return (
            ('2015', '2015'),
            ('2016', '2016'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                created_at__gte=date(int(self.value()), 1, 1),
                created_at__lte=date(int(self.value()), 12, 31)
            )


class TopicListFilter(admin.SimpleListFilter):
    title = 'topic'
    parameter_name = 'topic'

    def lookups(self, request, model_admin):
        return (
            ('python', 'Python'),
            ('ruby', 'Ruby'),
            ('java', 'Java'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(title__contains=self.value())


@admin.register(models.Course)  # register by decorator
class CourseAdmin(admin.ModelAdmin):
    # inlines = [TextInline, QuizInline, ]
    search_fields = ['title', 'description']
    list_filter = ['created_at', 'published', YearListFilter, TopicListFilter, ]
    list_display = [
        'title',
        'created_at',
        'published',
        'time_to_complete',  # the model's method
        'status',
    ]
    # list_editable = ['status']

    # sortable
    sortable_by = ('title', 'created_at',)
    ordering = ('created_at',)

    # actions
    actions = [make_published, make_in_review, make_in_progress]

    # display actions
    actions_on_top = True
    actions_on_bottom = True

    # customize edit page
    fields = (
        'title', 'subject', 'description', 'teacher',
        ('status', 'published',), 'created_at',  # tuple: one line
    )
    readonly_fields = ('created_at',)

    # for Markdown preview
    class Media:
        css = {'all': ('css/preview.css',)}
        js = ('js/vendor/marked.min.js', 'js/preview.js')


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline, ]
    search_fields = ['prompt']
    list_display = ['prompt', 'quiz', 'order']
    list_editable = ['quiz', 'order']
    # radio_fields = {'quiz': admin.HORIZONTAL}  # customizing for demo
    actions = ['delete_selected']  # globally disabled and allowed only in QuestionAdmin


class QuizAdmin(admin.ModelAdmin):
    fields = ['course', 'title', 'description', 'order', 'total_questions']
    search_fields = ['title', 'description']
    list_filter = ['course']
    list_display = ['title', 'course', 'number_correct_needed', 'total_questions']
    list_editable = ['course', 'total_questions']


class TextAdmin(admin.ModelAdmin):
    # fields = ['course', 'title', 'order', 'description', 'content']
    fieldsets = (
        (None, {'fields': ('course', 'title', 'order', 'description')}),
        ('Add content', {'fields': ('content',), 'classes': ('collapse',)}),
    )
    # radio_fields = {'course': admin.VERTICAL}  # customizing for demo

    # save button
    save_on_top = True


# admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Text, TextAdmin)
admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.MultipleChoiceQuestion, QuestionAdmin)
admin.site.register(models.TrueFalseQuestion, QuestionAdmin)
admin.site.register(models.Answer)

admin.site.site_title = 'Learning Site Administration'
admin.site.site_header = 'Learning Site Administration'
