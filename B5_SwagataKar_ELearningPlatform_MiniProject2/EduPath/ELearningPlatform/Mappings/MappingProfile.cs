using AutoMapper;
using ELearningPlatform.DTOs;
using ELearningPlatform.Models;

namespace ELearningPlatform.Mappings;

public class MappingProfile : Profile
{
    public MappingProfile()
    {
       
        CreateMap<User, UserResponseDto>();
        CreateMap<RegisterUserDto, User>()
            .ForMember(dest => dest.PasswordHash, opt => opt.Ignore());
        CreateMap<UpdateUserDto, User>();


        CreateMap<Course, CourseResponseDto>()
            .ForMember(dest => dest.CreatorName,
                opt => opt.MapFrom(src => src.Creator != null
                    ? src.Creator.FullName : ""))
            .ForMember(dest => dest.LessonCount,
                opt => opt.MapFrom(src => src.Lessons.Count))
            .ForMember(dest => dest.QuizCount,
                opt => opt.MapFrom(src => src.Quizzes.Count));
        CreateMap<CreateCourseDto, Course>();
        CreateMap<UpdateCourseDto, Course>();

        
        CreateMap<Lesson, LessonResponseDto>();
        CreateMap<CreateLessonDto, Lesson>();
        CreateMap<UpdateLessonDto, Lesson>();

        
        CreateMap<Quiz, QuizResponseDto>()
            .ForMember(dest => dest.CourseTitle,
                opt => opt.MapFrom(src => src.Course != null
                    ? src.Course.Title : ""))
            .ForMember(dest => dest.QuestionCount,
                opt => opt.MapFrom(src => src.Questions.Count));
        CreateMap<CreateQuizDto, Quiz>();

       
        CreateMap<Question, QuestionResponseDto>();
        CreateMap<CreateQuestionDto, Question>();

       
        CreateMap<Result, QuizResultResponseDto>()
            .ForMember(dest => dest.QuizTitle,
                opt => opt.MapFrom(src => src.Quiz != null
                    ? src.Quiz.Title : ""))
            .ForMember(dest => dest.CourseTitle,
                opt => opt.MapFrom(src => src.Quiz != null && src.Quiz.Course != null
                    ? src.Quiz.Course.Title : ""))
            .ForMember(dest => dest.TotalQuestions,
                opt => opt.MapFrom(src => src.Quiz != null
                    ? src.Quiz.Questions.Count : 0))
            .ForMember(dest => dest.Percentage, opt => opt.Ignore())
            .ForMember(dest => dest.Grade, opt => opt.Ignore())
            .ForMember(dest => dest.Status, opt => opt.Ignore())
            .ForMember(dest => dest.Feedback, opt => opt.Ignore());
    }
}