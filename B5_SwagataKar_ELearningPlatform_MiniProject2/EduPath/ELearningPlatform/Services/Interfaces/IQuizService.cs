using ELearningPlatform.DTOs;

namespace ELearningPlatform.Services.Interfaces;

public interface IQuizService
{
    Task<IEnumerable<QuizResponseDto>> GetByCourseIdAsync(int courseId);
    Task<IEnumerable<QuestionResponseDto>> GetQuestionsAsync(int quizId);
    Task<QuizResponseDto> CreateAsync(CreateQuizDto dto);
    Task<QuestionResponseDto> AddQuestionAsync(CreateQuestionDto dto);
    Task<QuizResultResponseDto> SubmitAsync(int quizId, SubmitQuizDto dto);
    Task<IEnumerable<QuizResultResponseDto>> GetResultsByUserAsync(int userId);
}