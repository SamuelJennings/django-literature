# from admin_extra_buttons.api import ExtraButtonsMixin, button
# from adminsortable2.admin import SortableAdminBase
# from django import forms
# from django.contrib import admin
# from django.shortcuts import redirect, render
# from django.utils.translation import gettext as _

# from .models import Collection, LiteratureItem, SupplementaryMaterial


# class LiteratureAdminAddForm(forms.ModelForm):
#     DOI = forms.CharField(label=_("DOI"), required=False)

#     class Meta:
#         model = LiteratureItem
#         fields = ["DOI"]


# class SupplementaryInline(admin.TabularInline):
#     model = SupplementaryMaterial
#     extra = 1


# @admin.register(LiteratureItem)
# class LiteratureAdmin(ExtraButtonsMixin, SortableAdminBase, admin.ModelAdmin):
#     """Django Admin setup for the `literature.LiteratureItem` model."""

#     # change_form_template = "admin/literature_change_form.html"
#     # form = LiteratureForm
#     list_display = ["file_download_link", "issued", "title", "citation_key", "type"]
#     list_filter = ["type"]
#     list_display_links = ["title"]
#     inlines = [SupplementaryInline]

#     @button(
#         html_attrs={"style": "background-color:var(--button-bg)"},
#         label=_("Fetch DOI"),
#         change_list=True,
#     )
#     def intermediate_form_view(self, request):
#         if request.method == "POST":
#             form = LiteratureAdminAddForm(request.POST)
#             if form.is_valid():
#                 return redirect("admin:literature_literatureitem_changelist")
#         else:
#             form = LiteratureAdminAddForm()

#         context = self.admin_site.each_context(request)
#         context["opts"] = self.model._meta
#         context["form"] = form
#         return render(request, "admin/literature_add_from.html", context)

#     def search_online(self, request, *args, **kwargs):
#         """Admin view that handles user-uploaded bibtex files

#         Returns:
#             HttpResponseRedirect: redirects to model admins change_list
#         """
#         if request.method == "POST":
#             form = OnlineSearchForm(request.POST)
#             if form.is_valid():
#                 bibliography = form.cleaned_data["CSL"]

#                 imported, updated = 0, 0
#                 for item in bibliography:
#                     imported += 1
#                     LiteratureItem.objects.create(CSL=item)
#                 self.message_user(
#                     request,
#                     level=messages.SUCCESS,
#                     message=(
#                         f"{imported} literature item{pluralize(imported)} {pluralize(imported,'was,were')} succesfully"
#                         f" imported and {updated} {pluralize(updated,'has,have')} been updated."
#                     ),
#                 )
#                 return HttpResponseRedirect("../")

#         else:
#             form = OnlineSearchForm(request.GET)

#         # return TemplateResponse(request, 'admin/change_form.html', {form: form})
#         return TemplateResponse(
#             request,
#             "literature/admin/search.html",
#             {
#                 "form": form,
#                 "opts": self.opts,
#             },
#         )


# @admin.register(Collection)
# class CollectionAdmin(admin.ModelAdmin):
#     pass
