from django.db import models


class Team(models.Model):
    name = models.CharField("Team Name", max_length=100)
    flag = models.CharField("Flag", max_length=10, db_index=True, blank=True)
    seq = models.IntegerField("Order Sequence", default=0)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        ordering = ["seq", "id"]

    def __str__(self):
        return str(self.name)


class Slot(models.Model):
    key = models.CharField("Slot Name", primary_key=True, max_length=50)
    chosen = models.ForeignKey(Team, null=True, blank=True)

    class Meta:
        verbose_name = "Slot"
        verbose_name_plural = "Slots"
        ordering = ["key"]

    def __str__(self):
        return str(self.key)
