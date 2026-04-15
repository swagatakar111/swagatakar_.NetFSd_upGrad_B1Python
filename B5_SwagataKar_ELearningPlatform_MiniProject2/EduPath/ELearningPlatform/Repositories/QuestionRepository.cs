using Microsoft.EntityFrameworkCore;
using ELearningPlatform.Data;
using ELearningPlatform.Models;
using ELearningPlatform.Repositories.Interfaces;

namespace ELearningPlatform.Repositories;

public class QuestionRepository : IQuestionRepository
{
    private readonly AppDbContext _context;
    public QuestionRepository(AppDbContext context) => _context = context;

    public async Task<IEnumerable<Question>> GetByQuizIdAsync(int quizId) =>
        await _context.Questions
            .AsNoTracking()
            .Where(q => q.QuizId == quizId)
            .ToListAsync();

    public async Task<Question?> GetByIdAsync(int id) =>
        await _context.Questions.AsNoTracking()
            .FirstOrDefaultAsync(q => q.QuestionId == id);

    public async Task<Question> CreateAsync(Question question)
    {
        _context.Questions.Add(question);
        await _context.SaveChangesAsync();
        return question;
    }
}