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


def validate_image_article_size(value):
    max_width = 1430
    max_height = 955
    min_width = 1420
    min_height = 945

    try:
        img = Image.open(value)
        width, height = img.size
        if width < min_width or height < min_height:
            raise ValidationError(
                f"Image is too small! Minimum size is {min_width}x{min_height}px."
            )
        if width > max_width or height > max_height:
            raise ValidationError(
                f"Image is too large! Maximum size is {max_width}x{max_height}px."
            )
    except Exception:
        raise ValidationError("Could not read image size.")
    
def validate_image_tutor_size(value):
    max_width = 490
    max_height = 490
    min_width = 480
    min_height = 480

    try:
        img = Image.open(value)
        width, height = img.size
        if width < min_width or height < min_height:
            raise ValidationError(
                f"Image is too small! Minimum size is {min_width}x{min_height}px."
            )
        if width > max_width or height > max_height:
            raise ValidationError(
                f"Image is too large! Maximum size is {max_width}x{max_height}px."
            )
    except Exception:
        raise ValidationError("Could not read image size.Image must be around 480<=width<=490 x 480<=height<=490px")
    
def validate_image_size(value):
    max_width = 380
    max_height = 250
    min_width = 370
    min_height = 240

    try:
        img = Image.open(value)
        width, height = img.size
        if width < min_width or height < min_height:
            raise ValidationError(
                f"Image is too small! Minimum size is {min_width}x{min_height}px."
            )
        if width > max_width or height > max_height:
            raise ValidationError(
                f"Image is too large! Maximum size is {max_width}x{max_height}px."
            )
    except Exception:
        raise ValidationError("Could not read image size.Image must be around 370<=width<=380 x 240<=height<=250px")



def validate_image_size_image(value):
    max_width = 620
    max_height = 530
    min_width = 610
    min_height = 525

    try:
        img = Image.open(value)
        width, height = img.size
        if width < min_width or height < min_height:
            raise ValidationError(
                f"Image is too small! Minimum size is {min_width}x{min_height}px."
            )
        if width > max_width or height > max_height:
            raise ValidationError(
                f"Image is too large! Maximum size is {max_width}x{max_height}px."
            )
    except Exception:
        raise ValidationError("Could not read image size.Image must be around 610<=width<=620 x 525<=height<=530px")


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
    image = models.ImageField(upload_to='pages/images/', null=True, blank=True,validators=[validate_image_format, validate_image_article_size])  # New image field
    created_at = models.DateTimeField(auto_now_add=True)  # New date field

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title
    



class Tutor(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    experience_years = models.PositiveIntegerField()
    lessons_completed = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)

    profile_image = models.ImageField(upload_to='tutors/', validators=[validate_image_format, validate_image_tutor_size], null=True, blank=True)  # New image field

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
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)  # Foreign key to Tutor
    course_type = models.CharField(max_length=100,blank=True)  # e.g., "Online", "In-person", "Hybrid"
    tags = models.TextField(blank=True)  # e.g., "English, Math, Science"
    duration = models.CharField(max_length=100)  # e.g., "4 weeks"
    weekly_study = models.CharField(max_length=100)  # e.g., "11 Hours"
    student_count = models.PositiveIntegerField()

    price = models.DecimalField(max_digits=8, decimal_places=2)  # e.g., 180.00
    payment_period = models.CharField(max_length=50, default="month")

    course_image = models.ImageField(upload_to='courses/images/', validators=[validate_image_format, validate_image_size_image], null=True, blank=True)
    preview_image = models.ImageField(upload_to='courses/images/',validators=[validate_image_format, validate_image_size], null=True, blank=True)  # New preview image field
    vimeo_url = models.URLField(blank=True, null=True)  # URL to the Vimeo video
    is_preview = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    overview = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)  # New date field

    def __str__(self):
        return self.title


class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(blank=True, default=1)


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


class Lecture(models.Model):
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE,related_name='lectures')
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    duration = models.DurationField()

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
