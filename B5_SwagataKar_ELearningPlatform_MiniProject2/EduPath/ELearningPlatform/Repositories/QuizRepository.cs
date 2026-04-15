using Microsoft.EntityFrameworkCore;
using ELearningPlatform.Data;
using ELearningPlatform.Models;
using ELearningPlatform.Repositories.Interfaces;

namespace ELearningPlatform.Repositories;

public class QuizRepository : IQuizRepository
{
    private readonly AppDbContext _context;
    public QuizRepository(AppDbContext context) => _context = context;

    public async Task<IEnumerable<Quiz>> GetByCourseIdAsync(int courseId) =>
        await _context.Quizzes
            .AsNoTracking()
            .Include(q => q.Course)
            .Include(q => q.Questions)
            .Where(q => q.CourseId == courseId)
            .ToListAsync();

    public async Task<Quiz?> GetByIdAsync(int id) =>
        await _context.Quizzes
            .AsNoTracking()
            .Include(q => q.Course)
            .Include(q => q.Questions)
            .FirstOrDefaultAsync(q => q.QuizId == id);

    public async Task<Quiz?> GetWithQuestionsAsync(int id) =>
        await _context.Quizzes
            .Include(q => q.Questions)
            .Include(q => q.Course)
            .FirstOrDefaultAsync(q => q.QuizId == id);

    public async Task<Quiz> CreateAsync(Quiz quiz)
    {
        _context.Quizzes.Add(quiz);
        await _context.SaveChangesAsync();
        return quiz;
    }

    public async Task<bool> ExistsAsync(int id) =>
        await _context.Quizzes.AnyAsync(q => q.QuizId == id);
}