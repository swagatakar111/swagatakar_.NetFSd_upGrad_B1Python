using Microsoft.EntityFrameworkCore;
using ELearningPlatform.Data;
using ELearningPlatform.Models;
using ELearningPlatform.Repositories.Interfaces;

namespace ELearningPlatform.Repositories;

public class LessonRepository : ILessonRepository
{
    private readonly AppDbContext _context;
    public LessonRepository(AppDbContext context) => _context = context;

    public async Task<IEnumerable<Lesson>> GetByCourseIdAsync(int courseId) =>
        await _context.Lessons
            .AsNoTracking()
            .Where(l => l.CourseId == courseId)
            .OrderBy(l => l.OrderIndex)
            .ToListAsync();

    public async Task<Lesson?> GetByIdAsync(int id) =>
        await _context.Lessons.AsNoTracking()
            .FirstOrDefaultAsync(l => l.LessonId == id);

    public async Task<Lesson> CreateAsync(Lesson lesson)
    {
        _context.Lessons.Add(lesson);
        await _context.SaveChangesAsync();
        return lesson;
    }

    public async Task<Lesson> UpdateAsync(Lesson lesson)
    {
        _context.Lessons.Update(lesson);
        await _context.SaveChangesAsync();
        return lesson;
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var lesson = await _context.Lessons.FindAsync(id);
        if (lesson == null) return false;
        _context.Lessons.Remove(lesson);
        await _context.SaveChangesAsync();
        return true;
    }
}