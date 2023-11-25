# yourapp/translation.py

from modeltranslation.translator import translator, TranslationOptions
from .models import TeamMember

class TeamMemberTranslationOptions(TranslationOptions):
    fields = ()

translator.register(TeamMember, TeamMemberTranslationOptions)
