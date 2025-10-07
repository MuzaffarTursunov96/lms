from django.db import models
from account.models import User
from datetime import timedelta
from PIL import Image
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
        verbose_name = _("Page Type")
        verbose_name_plural = _("Page Types")

    def __str__(self):
        return self.name


class BlogType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = _("Blog Type")
        verbose_name_plural = _("Blog Types")

    def __str__(self):
        return self.name
    

class Blogs(models.Model):
   
    title = models.CharField(_("Title"), max_length=200)
    page_type = models.ForeignKey(
        PageType, on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_("Page Type")
    )
    blog_type = models.ForeignKey(
        BlogType, on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_("Blog Type")
    )
    description = models.TextField(_("Description"))

    helper_text1 = models.TextField(_("Helper Text 1"), blank=True, null=True)
    helper_text2 = models.TextField(_("Helper Text 2"), blank=True, null=True)
    helper_text3 = models.TextField(_("Helper Text 3"), blank=True, null=True)
    helper_text4 = models.TextField(_("Helper Text 4"), blank=True, null=True)
    helper_text5 = models.TextField(_("Helper Text 5"), blank=True, null=True)

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    image = models.ImageField(
        _("Image"), upload_to='pages/images/', null=True, blank=True
    )
    vimeo_url = models.URLField(_("Vimeo URL"), blank=True, null=True)

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

    def __str__(self):
        return self.title




class Article(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))

    category = models.CharField(_("Category"), max_length=100, blank=True, null=True)
    start_date = models.DateField(_("Start Date"), blank=True, null=True)
    start_hour = models.TimeField(_("Start Hour"), blank=True, null=True)
    end_hour = models.TimeField(_("End Hour"), blank=True, null=True)
    topic = models.CharField(_("Topic"), max_length=200, blank=True, null=True)

    cost = models.DecimalField(_("Cost"), max_digits=10, decimal_places=2, default=0.00)

    organiser_full_name = models.CharField(_("Organiser Full Name"), max_length=200, blank=True, null=True)
    organiser_email = models.EmailField(_("Organiser Email"), blank=True, null=True)
    organiser_phone = models.CharField(_("Organiser Phone"), max_length=15, blank=True, null=True)

    helper_text1 = models.TextField(_("Helper Text 1"), blank=True, null=True)
    helper_text2 = models.TextField(_("Helper Text 2"), blank=True, null=True)
    helper_text3 = models.TextField(_("Helper Text 3"), blank=True, null=True)

    image = models.ImageField(_("Image"), upload_to='pages/images/', null=True, blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

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
    name = models.CharField(_("Name"), max_length=100)
    subject = models.CharField(_("Subject"), max_length=200)
    hourly_rate = models.DecimalField(_("Hourly Rate"), max_digits=6, decimal_places=2)
    experience_years = models.PositiveIntegerField(_("Experience (Years)"))
    lessons_completed = models.PositiveIntegerField(_("Lessons Completed"), default=0)
    rating = models.DecimalField(_("Rating"), max_digits=2, decimal_places=1, default=5.0)

    profile_image = models.ImageField(_("Profile Image"), upload_to='tutors/', null=True, blank=True)

    social_facebook = models.URLField(_("Facebook URL"), blank=True, null=True)
    social_twitter = models.URLField(_("Twitter URL"), blank=True, null=True)
    social_linkedin = models.URLField(_("LinkedIn URL"), blank=True, null=True)

    description = models.TextField(_("Description"), blank=True, null=True)
    helper_text1 = models.TextField(_("Helper Text 1"), blank=True, null=True)
    helper_text2 = models.TextField(_("Helper Text 2"), blank=True, null=True)
    helper_text3 = models.TextField(_("Helper Text 3"), blank=True, null=True)

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Tutor")
        verbose_name_plural = _("Tutors")

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
    tutor = models.ForeignKey(
        Tutor,
        on_delete=models.CASCADE,
        related_name='tutor_qualifications',
        verbose_name=_("Tutor"),
        blank=True,
        null=True
    )
    title = models.CharField(_("Title"), max_length=100)
    year = models.PositiveIntegerField(_("Year"))
    institution = models.CharField(_("Institution"), max_length=200)

    class Meta:
        verbose_name = _("Qualification")
        verbose_name_plural = _("Qualifications")

    def __str__(self):
        return f"{self.year} - {self.title} -{self.institution}"



class UserCourses(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        verbose_name=_("Course")
    )
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("User Course")
        verbose_name_plural = _("User Courses")

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

ACCORDION_DEFAULT_HTML = """
<div class="accordion accordion-style4" id="faqVersion2">
                        <div class="accordion-item active">
                            <div class="accordion-header" id="headingOne">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                    <span class="button-label">Week 1</span>
                                    Getting started with Extensive Reading
                                </button>
                            </div>
                            <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#faqVersion2">

                                <div class="accordion-body">
                                    <div class="syllabus-list">
                                        <div class="syllabus-img"><img src="assets/img/course/course-syllabus-1.jpg" alt=""></div>
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">Introduction</h6>
                                            <p class="syllabustext">Reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non proident.</p>
                                        </div>
                                    </div>
                                    <div class="syllabus-list">
                                        <div class="syllabus-img"><img src="assets/img/course/course-syllabus-2.jpg" alt=""></div>
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">What do you understand by Extensive Reading?</h6>
                                            <p class="syllabustext">Reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non proident.</p>
                                        </div>
                                    </div>
                                    <div class="syllabus-list">
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">Why Extensive Reading?</h6>
                                            <p class="syllabustext">Reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non illum dolore eu fugiat proident.</p>
                                        </div>
                                    </div>
                                    <div class="syllabus-list">
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">Incorporating Extensive Reading</h6>
                                            <p class="syllabustext">lit esse cillum dolore eu ferit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non illum dolore eu fugiat proident.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="accordion-item">
                            <div class="accordion-header" id="headingTwo">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                                    <span class="button-label">Week 2</span>
                                    Practical pre-reading activities with graded readers
                                </button>
                            </div>
                            <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#faqVersion2">

                                <div class="accordion-body">
                                    <div class="syllabus-list">
                                        <div class="syllabus-img"><img src="assets/img/course/course-syllabus-1.jpg" alt=""></div>
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">Introduction</h6>
                                            <p class="syllabustext">Reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non proident.</p>
                                        </div>
                                    </div>
                                    <div class="syllabus-list">
                                        <div class="syllabus-img"><img src="assets/img/course/course-syllabus-2.jpg" alt=""></div>
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">What do you understand by Extensive Reading?</h6>
                                            <p class="syllabustext">Reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non proident.</p>
                                        </div>
                                    </div>
                                    <div class="syllabus-list">
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">Why Extensive Reading?</h6>
                                            <p class="syllabustext">Reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non illum dolore eu fugiat proident.</p>
                                        </div>
                                    </div>
                                    <div class="syllabus-list">
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">Incorporating Extensive Reading</h6>
                                            <p class="syllabustext">lit esse cillum dolore eu ferit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non illum dolore eu fugiat proident.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="accordion-item">
                            <div class="accordion-header" id="headingThree">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                                    <span class="button-label">Week 3</span>
                                    Activities with graded readers
                                </button>
                            </div>
                            <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree" data-bs-parent="#faqVersion2">

                                <div class="accordion-body">
                                    <div class="syllabus-list">
                                        <div class="syllabus-img"><img src="assets/img/course/course-syllabus-1.jpg" alt=""></div>
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">Introduction</h6>
                                            <p class="syllabustext">Reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non proident.</p>
                                        </div>
                                    </div>
                                    <div class="syllabus-list">
                                        <div class="syllabus-img"><img src="assets/img/course/course-syllabus-2.jpg" alt=""></div>
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">What do you understand by Extensive Reading?</h6>
                                            <p class="syllabustext">Reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non proident.</p>
                                        </div>
                                    </div>
                                    <div class="syllabus-list">
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">Why Extensive Reading?</h6>
                                            <p class="syllabustext">Reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non illum dolore eu fugiat proident.</p>
                                        </div>
                                    </div>
                                    <div class="syllabus-list">
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">Incorporating Extensive Reading</h6>
                                            <p class="syllabustext">lit esse cillum dolore eu ferit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non illum dolore eu fugiat proident.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="accordion-item">
                            <div class="accordion-header" id="headingFour">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFour" aria-expanded="false" aria-controls="collapseFour">
                                    <span class="button-label">Week 4</span>
                                    Practical post-reading
                                </button>
                            </div>
                            <div id="collapseFour" class="accordion-collapse collapse" aria-labelledby="headingFour" data-bs-parent="#faqVersion2">

                                <div class="accordion-body">
                                    <div class="syllabus-list">
                                        <div class="syllabus-img"><img src="assets/img/course/course-syllabus-1.jpg" alt=""></div>
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">Introduction</h6>
                                            <p class="syllabustext">Reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non proident.</p>
                                        </div>
                                    </div>
                                    <div class="syllabus-list">
                                        <div class="syllabus-img"><img src="assets/img/course/course-syllabus-2.jpg" alt=""></div>
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">What do you understand by Extensive Reading?</h6>
                                            <p class="syllabustext">Reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non proident.</p>
                                        </div>
                                    </div>
                                    <div class="syllabus-list">
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">Why Extensive Reading?</h6>
                                            <p class="syllabustext">Reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non illum dolore eu fugiat proident.</p>
                                        </div>
                                    </div>
                                    <div class="syllabus-list">
                                        <div class="syllabus-content">
                                            <h6 class="syllabustitle">Incorporating Extensive Reading</h6>
                                            <p class="syllabustext">lit esse cillum dolore eu ferit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Ex cepteur sint upidatat non illum dolore eu fugiat proident.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
"""

class Course(models.Model):
    title = models.CharField(_("Title"),max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='courses', verbose_name=_("Tutor"),null=True, blank=True)  # Foreign key to Tutor
    course_type = models.CharField(_("Course Type"),max_length=100,blank=True)  # e.g., "Online", "In-person", "Hybrid"
    tags = models.TextField(_("Tags"),blank=True)  # e.g., "English, Math, Science"
    duration = models.CharField(_("Duration"),max_length=100)  # e.g., "4 weeks"
    weekly_study = models.CharField(max_length=100)  # e.g., "11 Hours"
    student_count = models.PositiveIntegerField()

    price = models.DecimalField(_("Price"),max_digits=8, decimal_places=2)  

    course_image = models.ImageField(_("Main Course Image"),upload_to='courses/images/',blank=True, null=True)
    preview_image = models.ImageField(_("Preview Image"),upload_to='courses/images/',blank=True, null=True)  # New preview image field
    vimeo_url = models.URLField(_("Vimeo URL"),blank=True, null=True)  # URL to the Vimeo video
    is_preview = models.BooleanField(_("Is Preview"),default=False)
    is_published = models.BooleanField(_("Is Published"),default=False)

    overview = models.TextField(_("Overview"),blank=True, null=True)
    # syllabus = models.TextField(_("Syllabus"), blank=True, null=True,default=ACCORDION_DEFAULT_HTML)
    syllabus = models.JSONField(_("Syllabus"),default=list, blank=True, null=True)
    outcomes = models.TextField(_("What Will You Achieve?"), blank=True, null=True)

    created_at = models.DateTimeField(_("Created At"),auto_now_add=True,blank=True, null=True)  # New date field


    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

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
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name=_("Course")
    )
    title = models.CharField(_("Title"), max_length=200)
    order = models.PositiveIntegerField(_("Order"), blank=True, default=1)

    class Meta:
        verbose_name = _("Course Section")
        verbose_name_plural = _("Course Sections")
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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        blank=True,
        null=True
    )
    lecture = models.ForeignKey(
        "Lecture",
        on_delete=models.CASCADE,
        verbose_name=_("Lecture"),
        blank=True,
        null=True
    )
    watched_seconds = models.FloatField(_("Watched Seconds"), default=0)
    watched_percent = models.FloatField(_("Watched Percent"), default=0)
    updated_at = models.DateTimeField(_("Last Updated"), auto_now=True)


    class Meta:
        verbose_name = _("Lecture Progress")
        verbose_name_plural = _("Lecture Progresses")
        unique_together = ('user', 'lecture')


class Lecture(models.Model):
    section = models.ForeignKey(
        CourseSection,
        on_delete=models.CASCADE,
        related_name='lectures',
        verbose_name=_("Course Section")
    )
    title = models.CharField(_("Title"), max_length=255)
    video_url = models.URLField(_("Video URL"))
    duration = models.DurationField(_("Duration"))
    order = models.PositiveIntegerField(_("Order"), blank=True, null=True)

    class Meta:
        verbose_name = _("Lecture")
        verbose_name_plural = _("Lectures")
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
    section = models.ForeignKey(
        CourseSection,
        on_delete=models.CASCADE,
        related_name='bullet_points',
        verbose_name=_("Course Section")
    )
    text = models.CharField(_("Text"), max_length=255)

    class Meta:
        verbose_name = _("Course Bullet Point")
        verbose_name_plural = _("Course Bullet Points")

    def __str__(self):
        return self.text
    



class Review(models.Model):
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_("Course")
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    rating = models.IntegerField(
        _("Rating"),
        choices=[(i, i) for i in range(1, 6)]
    )
    comment = models.TextField(_("Comment"))
    show = models.BooleanField(_("Show on site"), default=False, blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ['-created_at']