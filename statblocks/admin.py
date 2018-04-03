from django.contrib import admin

from statblocks.models import Monster, MonsterForm


class MonsterAdmin(admin.ModelAdmin):
    form = MonsterForm


admin.site.register(Monster, MonsterAdmin)
