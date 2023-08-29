from django.contrib import admin

from .models import Category, Entertaiment, Likers

# Register your models here.
 
class CategoryAdmin(admin.ModelAdmin):
	...

class EntertainmentAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'created_at', 'is_published']
	list_display_links = 'title', 'created_at'
	search_fields = 'id', 'title', 'description', 'slug', 'review'
	list_filter = 'category', 'author', 'is_published', 'review_is_html'
	list_per_page = 10
	list_editable = 'is_published',
	ordering = 'id',
	prepopulated_fields = {
		"slug": ('title',)
	}

class LikersAdmin(admin.ModelAdmin):
    	...

admin.site.register(Category, CategoryAdmin) 
admin.site.register(Entertaiment, EntertainmentAdmin) 
admin.site.register(Likers, LikersAdmin) 
