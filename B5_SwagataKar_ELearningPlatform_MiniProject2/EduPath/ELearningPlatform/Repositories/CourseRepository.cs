using Microsoft.EntityFrameworkCore;
using ELearningPlatform.Data;
using ELearningPlatform.Models;
using ELearningPlatform.Repositories.Interfaces;

namespace ELearningPlatform.Repositories;

public class CourseRepository : ICourseRepository
{
    private readonly AppDbContext _context;
    public CourseRepository(AppDbContext context) => _context = context;

    public async Task<IEnumerable<Course>> GetAllAsync() =>
        await _context.Courses
            .AsNoTracking()
            .Include(c => c.Creator)
            .Include(c => c.Lessons)
            .Include(c => c.Quizzes)
            .ToListAsync();

    public async Task<Course?> GetByIdAsync(int id) =>
        await _context.Courses
            .AsNoTracking()
            .Include(c => c.Creator)
            .Include(c => c.Lessons)
            .Include(c => c.Quizzes)
            .FirstOrDefaultAsync(c => c.CourseId == id);

    public async Task<Course> CreateAsync(Course course)
    {
        _context.Courses.Add(course);
        await _context.SaveChangesAsync();
        return course;
    }

    public async Task<Course> UpdateAsync(Course course)
    {
        _context.Courses.Update(course);
        await _context.SaveChangesAsync();
        return course;
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var course = await _context.Courses.FindAsync(id);
        if (course == null) return false;
        _context.Courses.Remove(course);
        await _context.SaveChangesAsync();
        return true;
    }

    public async Task<bool> ExistsAsync(int id) =>
        await _context.Courses.AnyAsync(c => c.CourseId == id);
}