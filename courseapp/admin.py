from django.contrib import admin
from .models import UserProfile, Course, Video

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_user_email', 'flag', 'batch_number')
    search_fields = ('user__username', 'user__email')
    list_filter = ('flag',)
    fields = ('user', 'flag', 'batch_number')

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User Email'

    def get_flag_display(self, obj):
        flag_display = {
            -1: 'Negative One',
            0: 'Zero',
            1: 'One',
            2: 'Two',
        }
        return flag_display.get(obj.flag, 'Unknown')
    get_flag_display.short_description = 'Flag Display'

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'flag':
            kwargs['choices'] = [
                (-1, 'Negative One'),
                (0, 'Zero'),
                (1, 'One'),
                (2, 'Two'),
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

admin.site.register(UserProfile, UserProfileAdmin)

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [VideoInline]
    list_display = ('title', 'batch_number')  # Add batch number to list display
    search_fields = ('title',)
    list_filter = ( 'batch_number',)  # Add batch number to filters

admin.site.register(Course, CourseAdmin)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title',)
    Description = ('Description',)

admin.site.register(Video, VideoAdmin)
