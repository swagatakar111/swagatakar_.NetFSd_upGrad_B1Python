using Microsoft.EntityFrameworkCore;
using ELearningPlatform.Data;
using ELearningPlatform.Models;
using ELearningPlatform.Repositories.Interfaces;

namespace ELearningPlatform.Repositories;

public class ResultRepository : IResultRepository
{
    private readonly AppDbContext _context;
    public ResultRepository(AppDbContext context) => _context = context;

    public async Task<IEnumerable<Result>> GetByUserIdAsync(int userId) =>
        await _context.Results
            .AsNoTracking()
            .Include(r => r.Quiz)
                .ThenInclude(q => q!.Course)
            .Include(r => r.Quiz)
                .ThenInclude(q => q!.Questions)
            .Where(r => r.UserId == userId)
            .OrderByDescending(r => r.AttemptDate)
            .ToListAsync();

    public async Task<Result?> GetByUserAndQuizAsync(int userId, int quizId) =>
        await _context.Results
            .AsNoTracking()
            .FirstOrDefaultAsync(r => r.UserId == userId && r.QuizId == quizId);

    public async Task<Result> CreateAsync(Result result)
    {
        _context.Results.Add(result);
        await _context.SaveChangesAsync();
        return result;
    }

    public async Task<double> GetAverageScoreAsync() =>
        await _context.Results.AnyAsync()
            ? await _context.Results.AverageAsync(r => r.Score)
            : 0;
}