using AutoMapper;
using ELearningPlatform.DTOs;
using ELearningPlatform.Models;
using ELearningPlatform.Repositories.Interfaces;
using ELearningPlatform.Services.Interfaces;

namespace ELearningPlatform.Services;

public class QuizService : IQuizService
{
    private readonly IQuizRepository _quizRepo;
    private readonly IQuestionRepository _questionRepo;
    private readonly IResultRepository _resultRepo;
    private readonly IMapper _mapper;

    public QuizService(
        IQuizRepository quizRepo,
        IQuestionRepository questionRepo,
        IResultRepository resultRepo,
        IMapper mapper)
    {
        _quizRepo = quizRepo;
        _questionRepo = questionRepo;
        _resultRepo = resultRepo;
        _mapper = mapper;
    }

    public async Task<IEnumerable<QuizResponseDto>> GetByCourseIdAsync(int courseId)
    {
        var quizzes = await _quizRepo.GetByCourseIdAsync(courseId);
        return _mapper.Map<IEnumerable<QuizResponseDto>>(quizzes);
    }

    public async Task<IEnumerable<QuestionResponseDto>> GetQuestionsAsync(int quizId)
    {
        var questions = await _questionRepo.GetByQuizIdAsync(quizId);
        return _mapper.Map<IEnumerable<QuestionResponseDto>>(questions);
    }

    public async Task<QuizResponseDto> CreateAsync(CreateQuizDto dto)
    {
        var quiz = _mapper.Map<Quiz>(dto);
        var created = await _quizRepo.CreateAsync(quiz);
        var withDetails = await _quizRepo.GetByIdAsync(created.QuizId);
        return _mapper.Map<QuizResponseDto>(withDetails!);
    }

    public async Task<QuestionResponseDto> AddQuestionAsync(CreateQuestionDto dto)
    {
        var question = _mapper.Map<Question>(dto);
        var created = await _questionRepo.CreateAsync(question);
        return _mapper.Map<QuestionResponseDto>(created);
    }

    public async Task<QuizResultResponseDto> SubmitAsync(int quizId, SubmitQuizDto dto)
    {
        var quiz = await _quizRepo.GetWithQuestionsAsync(quizId)
            ?? throw new KeyNotFoundException($"Quiz {quizId} not found.");

        if (!quiz.Questions.Any())
            throw new InvalidOperationException("This quiz has no questions.");

       
        int score = 0;
        foreach (var question in quiz.Questions)
        {
            if (dto.Answers.TryGetValue(question.QuestionId, out var userAnswer))
            {
                if (userAnswer.ToUpper() == question.CorrectAnswer.ToUpper())
                    score++;
            }
        }

        
        var result = new Result
        {
            UserId = dto.UserId,
            QuizId = quizId,
            Score = score,
            AttemptDate = DateTime.UtcNow
        };
        var saved = await _resultRepo.CreateAsync(result);

        
        int total = quiz.Questions.Count;
        double percent = total > 0
            ? Math.Round((double)score / total * 100, 1) : 0;

        return new QuizResultResponseDto
        {
            ResultId = saved.ResultId,
            UserId = dto.UserId,
            QuizId = quizId,
            QuizTitle = quiz.Title,
            CourseTitle = quiz.Course?.Title ?? "",
            Score = score,
            TotalQuestions = total,
            Percentage = percent,
            Grade = GetGrade(percent),
            Status = percent >= 40 ? "Pass" : "Fail",
            Feedback = GetFeedback(percent),
            AttemptDate = saved.AttemptDate
        };
    }

    public async Task<IEnumerable<QuizResultResponseDto>> GetResultsByUserAsync(int userId)
    {
        var results = await _resultRepo.GetByUserIdAsync(userId);

        return results.Select(r =>
        {
            int total = r.Quiz?.Questions.Count ?? 0;
            double percent = total > 0
                ? Math.Round((double)r.Score / total * 100, 1) : 0;

            return new QuizResultResponseDto
            {
                ResultId = r.ResultId,
                UserId = r.UserId,
                QuizId = r.QuizId,
                QuizTitle = r.Quiz?.Title ?? "",
                CourseTitle = r.Quiz?.Course?.Title ?? "",
                Score = r.Score,
                TotalQuestions = total,
                Percentage = percent,
                Grade = GetGrade(percent),
                Status = percent >= 40 ? "Pass" : "Fail",
                Feedback = GetFeedback(percent),
                AttemptDate = r.AttemptDate
            };
        });
    }

    private static string GetGrade(double percent) => percent switch
    {
        >= 80 => "A",
        >= 60 => "B",
        >= 40 => "C",
        _ => "F"
    };

    private static string GetFeedback(double percent) => GetGrade(percent) switch
    {
        "A" => "Outstanding performance! Excellent work!",
        "B" => "Good job! You have a solid understanding.",
        "C" => "Average. Review the material and try again.",
        _ => "Needs improvement. Please revisit the lessons."
    };
}