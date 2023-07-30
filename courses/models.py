from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from  accounts.models import TimeStamp
import secrets, uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from config.utils import get_cover_upload_to, get_image_upload_to
from django.db.models import Sum, Avg, Count

User = get_user_model()


class Category(TimeStamp):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(unique=True, blank=True)
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + '-' + str(uuid.uuid4())[:8]
        while Category.objects.filter(slug=self.slug).exists():
            self.slug = slugify(self.title) + '-' + str(uuid.uuid4())[:10]
        super(Category, self).save(*args, **kwargs)

    @property
    def num_courses(self):
        return self.courses.count()
    

class Course(TimeStamp):
    COURSE_TYPE_CHOICES = (
        ('Free', 'Free'),
        ('Paid', 'Paid'),
    )

    title = models.CharField(max_length=255)
    code = models.CharField(max_length=8, unique=True, editable=False,)
    image = models.ImageField(upload_to=get_image_upload_to, null=True, blank=True)
    cover = models.ImageField(upload_to=get_cover_upload_to, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price_before_discount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    course_type = models.CharField(max_length=4, choices=COURSE_TYPE_CHOICES, default='Free')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE,
                                    limit_choices_to={'groups__name': 'Instructor'})
    is_online = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    categories = models.ManyToManyField(Category, related_name='courses', blank=True)
    keywords = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a random code if the object is being created
            self.code = secrets.token_hex(4).upper()  # Generate 4 bytes of randomness and convert to uppercase hex string
            while Course.objects.filter(code=self.code).exists():
                # Regenerate the code if it's not unique
                self.code = secrets.token_hex(4).upper()

        self.slug = slugify(self.title) + '-' + str(uuid.uuid4())[:8]
        while Course.objects.filter(slug=self.slug).exists():
            self.slug = slugify(self.title) + '-' + str(uuid.uuid4())[:10]
        super(Course, self).save(*args, **kwargs)

    @property
    def get_duration(self):
        try:
            return (self.end_date - self.start_date).days
        except:
            return 0
        
    @property
    def get_lessons(self):
        try:
            return len(self.lessons.all())
        except:
            return 0
        
    @property
    def get_total_students(self):    
        total_students = Lesson.objects.filter(lesson__course__id=self.id).aggregate(Sum('students'))['students__sum']
        return total_students
    
    @property
    def get_course_reviews(self):
        reviews = Review.objects.filter(course__id=self.id)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        num_reviews = reviews.aggregate(Count('id'))['id__count']
        return (avg_rating, num_reviews)

class Lesson(TimeStamp):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    video_url = models.URLField(null=True, blank=True)
    video_file = models.FileField(upload_to='lesson_videos/', null=True, blank=True)
    transcript = models.TextField()
    duration = models.DurationField()
    notes = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE,
                                    limit_choices_to={'groups__name': 'Instructor'})
    students = models.ManyToManyField(User, related_name='lessons_enrolled_in',
                                      limit_choices_to={'groups__name': 'Student'})
    
    def __str__(self) -> str:
        return self.title
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + '-' + str(uuid.uuid4())[:8]
        while Course.objects.filter(slug=self.slug).exists():
            self.slug = slugify(self.title) + '-' + str(uuid.uuid4())[:10]
        super(Lesson, self).save(*args, **kwargs)


class Comment(TimeStamp):
    text = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
    

    def __str__(self) -> str:
        return 'comment by {}'.format(self.user.full_name)
    

class Review(TimeStamp):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    