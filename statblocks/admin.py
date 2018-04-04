from django.contrib import admin

from statblocks.models import SpecialProperty, SpecialPropertyForm, \
    Action, ActionForm, LegendaryAction, LegendaryActionForm, Reaction, ReactionForm


class SpecialPropertyAdmin(admin.ModelAdmin):
    form = SpecialPropertyForm


class ActionAdmin(admin.ModelAdmin):
    form = ActionForm


class LegendaryActionAdmin(admin.ModelAdmin):
    form = LegendaryActionForm


class ReactionAdmin(admin.ModelAdmin):
    form = ReactionForm


admin.site.register(SpecialProperty, SpecialPropertyAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(LegendaryAction, LegendaryActionAdmin)
admin.site.register(Reaction, ReactionAdmin)
