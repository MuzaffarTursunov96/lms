from django.db import models
from account.models import User
from datetime import timedelta
from PIL import Image
from django.core.exceptions import ValidationError
# Create your models here.


def validate_image_format(value):
    valid_formats = ['JPEG', 'JPG', 'PNG','jpeg', 'jpg', 'png']
    try:
        img = Image.open(value)
        if img.format.upper() not in valid_formats:
            raise ValidationError("Only JPG and PNG images are allowed.")
    except Exception:
        raise ValidationError("Invalid image file.")








class PageType(models.Model):
    name = models.CharField(max_length=100, unique=True)
   
    class Meta:
        verbose_name = "Page Type"
        verbose_name_plural = "Page Types"

    def __str__(self):
        return self.name


class BlogType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = "Blog Type"
        verbose_name_plural = "Blog Types"

    def __str__(self):
        return self.name
    

class Blogs(models.Model):
   
    title = models.CharField(max_length=200)
    page_type = models.ForeignKey(PageType, on_delete=models.SET_NULL, null=True, blank=True)
    blog_type = models.ForeignKey(BlogType, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    helper_text1 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text2 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text3 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text4 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text5 = models.TextField(blank=True, null=True)  # New helper text field
    created_at = models.DateTimeField(auto_now_add=True)  # New date field
    image = models.ImageField(upload_to='pages/images/', null=True, blank=True)  # New image field
    vimeo_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title




class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)  # New category field
    start_date = models.DateField(blank=True, null=True) 
    start_hour = models.TimeField(blank=True, null=True)
    end_hour = models.TimeField(blank=True, null=True)
    topic = models.CharField(max_length=200, blank=True, null=True) 
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    organiser_full_name =  models.CharField(max_length=200, blank=True, null=True)
    organiser_email = models.EmailField(blank=True, null=True)
    organiser_phone = models.CharField(max_length=15, blank=True, null=True)
    helper_text1 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text2 = models.TextField(blank=True, null=True)  # New helper text
    helper_text3 = models.TextField(blank=True, null=True)  # New helper text field
    image = models.ImageField(upload_to='pages/images/', null=True, blank=True)  # New image field
    created_at = models.DateTimeField(auto_now_add=True)  # New date field

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Save first so we have self.profile_image.path
        super().save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)

            # Convert to RGB if needed (to avoid issues with PNG/alpha when saving as JPEG)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Resize while keeping aspect ratio
            max_size = (1425, 950)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Save back to same path (JPEG quality applies only to JPG files)
            img.save(img_path, optimize=True, quality=90)
    



class Tutor(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    experience_years = models.PositiveIntegerField()
    lessons_completed = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)

    profile_image = models.ImageField(upload_to='tutors/', null=True, blank=True)  # New image field

    social_facebook = models.URLField(blank=True, null=True)
    social_twitter = models.URLField(blank=True, null=True)
    social_linkedin = models.URLField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    helper_text1 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text2 = models.TextField(blank=True, null=True)  # New helper text field
    helper_text3 = models.TextField(blank=True, null=True)  # New helper text field
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)  # New date field
    

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Save the original first
        super().save(*args, **kwargs)

        if self.profile_image:
            img_path = self.profile_image.path
            img = Image.open(img_path)

            # Convert to RGB if needed (to avoid issues with PNG/alpha when saving as JPEG)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Resize while keeping aspect ratio
            max_size = (490, 490)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Save back to same path (JPEG quality applies only to JPG files)
            img.save(img_path, optimize=True, quality=90)


class Qualification(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='tutor_qualifications',blank=True,null=True)
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    institution = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.year} - {self.title} -{self.institution}"



class UserCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"



class Course(models.Model):
    title = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)  # Foreign key to Tutor
    course_type = models.CharField(max_length=100,blank=True)  # e.g., "Online", "In-person", "Hybrid"
    tags = models.TextField(blank=True)  # e.g., "English, Math, Science"
    duration = models.CharField(max_length=100)  # e.g., "4 weeks"
    weekly_study = models.CharField(max_length=100)  # e.g., "11 Hours"
    student_count = models.PositiveIntegerField()

    price = models.DecimalField(max_digits=8, decimal_places=2)  

    course_image = models.ImageField(upload_to='courses/images/',blank=True, null=True)
    preview_image = models.ImageField(upload_to='courses/images/',blank=True, null=True)  # New preview image field
    vimeo_url = models.URLField(blank=True, null=True)  # URL to the Vimeo video
    is_preview = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    overview = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)  # New date field

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        # Save first so we have self.profile_image.path
        super().save(*args, **kwargs)

        if self.course_image:
            img_path = self.course_image.path
            img = Image.open(img_path)

            # Convert to RGB if needed (to avoid issues with PNG/alpha when saving as JPEG)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Resize while keeping aspect ratio
            max_size = (615, 525)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Save back to same path (JPEG quality applies only to JPG files)
            img.save(img_path, optimize=True, quality=90)
        
        if self.preview_image:
            img_path = self.preview_image.path
            img = Image.open(img_path)

            # Convert to RGB if needed (to avoid issues with PNG/alpha when saving as JPEG)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Resize while keeping aspect ratio
            max_size = (375, 245)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Save back to same path (JPEG quality applies only to JPG files)
            img.save(img_path, optimize=True, quality=90)


class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(blank=True, default=1)

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if self.order is None:
            last_order = CourseSection.objects.filter(course=self.course).aggregate(models.Max("order"))["order__max"]
            self.order = 1 if last_order is None else last_order + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def total_duration(self):
        total = timedelta()
        # We can access the lectures in this specific section using 'lectures'
        # because of the `related_name` on the Lecture model's ForeignKey
        for lecture in self.lectures.all():
            if lecture.duration:
                total += lecture.duration
        return total

    @property
    def formatted_total_duration(self):
        # This property formats the total duration into a readable string
        total_seconds = int(self.total_duration.total_seconds())
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return f"{minutes:02}:{seconds:02}"
    

class LectureProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    lecture = models.ForeignKey("Lecture", on_delete=models.CASCADE,blank=True, null=True)
    watched_seconds = models.FloatField(default=0)
    watched_percent = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lecture')


class Lecture(models.Model):
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE,related_name='lectures')
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    duration = models.DurationField()
    order = models.PositiveIntegerField(blank=True, null=True)  # new field

    class Meta:
        ordering = ["order"]  # always sort by order

    def save(self, *args, **kwargs):
        if self.order is None:
            # get max order in this section
            last_order = Lecture.objects.filter(section=self.section).aggregate(models.Max("order"))["order__max"]
            self.order = 1 if last_order is None else last_order + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def formatted_duration(self):
        if self.duration is None:
            return ""
        total_seconds = int(self.duration.total_seconds())
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return f"{minutes:02}:{seconds:02}"

class CourseBulletPoint(models.Model):
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='bullet_points')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    



class Review(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    comment = models.TextField()
    show = models.BooleanField(default=False,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
