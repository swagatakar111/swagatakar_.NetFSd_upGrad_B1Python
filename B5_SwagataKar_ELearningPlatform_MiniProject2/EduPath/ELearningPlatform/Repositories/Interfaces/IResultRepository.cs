using ELearningPlatform.Models;

namespace ELearningPlatform.Repositories.Interfaces;

public interface IResultRepository
{
    Task<IEnumerable<Result>> GetByUserIdAsync(int userId);
    Task<Result?> GetByUserAndQuizAsync(int userId, int quizId);
    Task<Result> CreateAsync(Result result);
    Task<double> GetAverageScoreAsync();
}