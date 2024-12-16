from django.db import models
from django.utils.text import slugify

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  # Add Slug field
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Automatically create a slug from the title
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        # Automatically set the order to the next available position
        if not self.order:
            last_chapter = Chapter.objects.filter(course=self.course).order_by('-order').first()
            if last_chapter:
                self.order = last_chapter.order + 1  # Set to the next order
            else:
                self.order = 1  # If no chapters exist, set to 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} (Chapter:{self.course.title})"

class Section(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    order = models.PositiveBigIntegerField()

    def save(self, *args, **kwargs):
        # Automatically set the order to the next available position in the chapter
        if not self.order:
            last_section = Section.objects.filter(chapter=self.chapter).order_by('-order').first()
            if last_section:
                self.order = last_section.order + 1  # Set to the next order
            else:
                self.order = 1  # If no sections exist, set to 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} (Section:{self.chapter.title})"


class Note(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  # Add Slug field
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Automatically create a slug from the title
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} (Note:{self.section.title})"