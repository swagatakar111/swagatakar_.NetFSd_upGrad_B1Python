using Microsoft.AspNetCore.Mvc;
using ELearningPlatform.DTOs;
using ELearningPlatform.Services.Interfaces;

namespace ELearningPlatform.Controllers;

[ApiController]
[Route("api/quizzes")]
public class QuizzesController : ControllerBase
{
    private readonly IQuizService _service;
    public QuizzesController(IQuizService service) => _service = service;

   
    [HttpGet("{courseId}")]
    public async Task<IActionResult> GetByCourse(int courseId)
    {
        var quizzes = await _service.GetByCourseIdAsync(courseId);
        return Ok(quizzes);
    }

  
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateQuizDto dto)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        var created = await _service.CreateAsync(dto);
        return StatusCode(201, created);
    }

  
    [HttpGet("{quizId}/questions")]
    public async Task<IActionResult> GetQuestions(int quizId)
    {
        try
        {
            var questions = await _service.GetQuestionsAsync(quizId);
            return Ok(questions);
        }
        catch (KeyNotFoundException ex)
        {
            return NotFound(new { message = ex.Message });
        }
    }


    [HttpPost("/api/questions")]
    public async Task<IActionResult> AddQuestion([FromBody] CreateQuestionDto dto)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        var created = await _service.AddQuestionAsync(dto);
        return StatusCode(201, created);
    }


    [HttpPost("{quizId}/submit")]
    public async Task<IActionResult> Submit(int quizId, [FromBody] SubmitQuizDto dto)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        try
        {
            var result = await _service.SubmitAsync(quizId, dto);
            return Ok(result);
        }
        catch (KeyNotFoundException ex)
        {
            return NotFound(new { message = ex.Message });
        }
        catch (InvalidOperationException ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }
}