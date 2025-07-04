from django.contrib import admin
from .models import Human, Image, Incident, IncidentDetail


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    fields = ("image_url", "image_type", "added_on", "incident")
    readonly_fields = ("added_on",)
    show_change_link = True


class IncidentDetailInline(admin.TabularInline):
    model = IncidentDetail
    extra = 0
    fields = ("timestamp", "status", "image", "humans_list")
    readonly_fields = ("timestamp", "humans_list")
    filter_horizontal = ("humans",)

    # Handy display for linked people
    def humans_list(self, obj):
        return ", ".join(h.name or str(h.id) for h in obj.humans.all())

    humans_list.short_description = "Humans"


@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "human_type_display",
        "email",
        "phone",
        "created_on",
    )
    list_filter = ("human_type", "created_on")
    search_fields = ("name", "email", "phone")
    inlines = [ImageInline]
    readonly_fields = ("created_on", "updated_on")

    def human_type_display(self, obj):
        return obj.get_human_type_display()

    human_type_display.short_description = "Type"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "thumbnail",
        "image_type_display",
        "human",
        "incident",
        "added_on",
    )
    list_filter = ("image_type", "added_on")
    search_fields = ("image_url",)
    readonly_fields = ("added_on",)

    def image_type_display(self, obj):
        return obj.get_image_type_display()

    image_type_display.short_description = "Type"


    def thumbnail(self, obj):
        return (
            f'<a href="{obj.image_url}" target="_blank">'
            f'<img src="{obj.image_url}" style="height:40px;" />'
            "</a>"
        )

    thumbnail.allow_tags = True
    thumbnail.short_description = "Preview"


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status_display",
        "start_on",
        "end_on",
        "video_clip",
        "best_image",
        "humans_summary",
    )
    list_filter = ("status", "start_on")
    date_hierarchy = "start_on"
    search_fields = ("id",)
    inlines = [IncidentDetailInline]
    filter_horizontal = ("humans",)
    readonly_fields = ("start_on", "end_on")

    def status_display(self, obj):
        return obj.get_status_display()

    status_display.short_description = "Status"

    def humans_summary(self, obj):
        return ", ".join(h.name or str(h.id) for h in obj.humans.all()[:5]) + (
            "…" if obj.humans.count() > 5 else ""
        )

    humans_summary.short_description = "Humans"


@admin.register(IncidentDetail)
class IncidentDetailAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "incident",
        "status_display",
        "timestamp",
        "image",
        "humans_summary",
    )
    list_filter = ("status", "timestamp")
    date_hierarchy = "timestamp"
    search_fields = ("incident__id",)
    filter_horizontal = ("humans",)
    readonly_fields = ("timestamp",)

    def status_display(self, obj):
        return obj.get_status_display()

    status_display.short_description = "Status"

    def humans_summary(self, obj):
        return ", ".join(h.name or str(h.id) for h in obj.humans.all())

    humans_summary.short_description = "Humans"
