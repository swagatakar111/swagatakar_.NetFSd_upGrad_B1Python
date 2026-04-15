using Microsoft.EntityFrameworkCore;
using ELearningPlatform.Models;

namespace ELearningPlatform.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<User> Users => Set<User>();
    public DbSet<Course> Courses => Set<Course>();
    public DbSet<Lesson> Lessons => Set<Lesson>();
    public DbSet<Quiz> Quizzes => Set<Quiz>();
    public DbSet<Question> Questions => Set<Question>();
    public DbSet<Result> Results => Set<Result>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

       
        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(u => u.UserId);
            entity.HasIndex(u => u.Email).IsUnique();
            entity.Property(u => u.FullName).IsRequired().HasMaxLength(100);
            entity.Property(u => u.Email).IsRequired().HasMaxLength(150);
            entity.Property(u => u.PasswordHash).IsRequired();
        });

       
        modelBuilder.Entity<Course>(entity =>
        {
            entity.HasKey(c => c.CourseId);
            entity.Property(c => c.Title).IsRequired().HasMaxLength(200);
            entity.Property(c => c.Description).HasMaxLength(1000);

          
            entity.HasOne(c => c.Creator)
                  .WithMany(u => u.Courses)
                  .HasForeignKey(c => c.CreatedBy)
                  .OnDelete(DeleteBehavior.Restrict);
        });

       
        modelBuilder.Entity<Lesson>(entity =>
        {
            entity.HasKey(l => l.LessonId);
            entity.Property(l => l.Title).IsRequired().HasMaxLength(200);

           
            entity.HasOne(l => l.Course)
                  .WithMany(c => c.Lessons)
                  .HasForeignKey(l => l.CourseId)
                  .OnDelete(DeleteBehavior.Cascade);
        });

      
        modelBuilder.Entity<Quiz>(entity =>
        {
            entity.HasKey(q => q.QuizId);
            entity.Property(q => q.Title).IsRequired().HasMaxLength(200);

            
            entity.HasOne(q => q.Course)
                  .WithMany(c => c.Quizzes)
                  .HasForeignKey(q => q.CourseId)
                  .OnDelete(DeleteBehavior.Cascade);
        });

      
        modelBuilder.Entity<Question>(entity =>
        {
            entity.HasKey(q => q.QuestionId);
            entity.Property(q => q.QuestionText).IsRequired();
            entity.Property(q => q.CorrectAnswer).IsRequired().HasMaxLength(1);

           
            entity.HasOne(q => q.Quiz)
                  .WithMany(qz => qz.Questions)
                  .HasForeignKey(q => q.QuizId)
                  .OnDelete(DeleteBehavior.Cascade);
        });

      
        modelBuilder.Entity<Result>(entity =>
        {
            entity.HasKey(r => r.ResultId);

            
            entity.HasOne(r => r.User)
                  .WithMany(u => u.Results)
                  .HasForeignKey(r => r.UserId)
                  .OnDelete(DeleteBehavior.Restrict);

            
            entity.HasOne(r => r.Quiz)
                  .WithMany(q => q.Results)
                  .HasForeignKey(r => r.QuizId)
                  .OnDelete(DeleteBehavior.Restrict);
        });
    }
}