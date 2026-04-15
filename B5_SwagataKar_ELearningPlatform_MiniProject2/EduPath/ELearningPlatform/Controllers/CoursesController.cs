using Microsoft.AspNetCore.Mvc;
using ELearningPlatform.DTOs;
using ELearningPlatform.Services.Interfaces;

namespace ELearningPlatform.Controllers;

[ApiController]
[Route("api/courses")]
public class CoursesController : ControllerBase
{
    private readonly ICourseService _service;
    private readonly ILessonService _lessonService;

    public CoursesController(ICourseService service, ILessonService lessonService)
    {
        _service = service;
        _lessonService = lessonService;
    }

    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        var courses = await _service.GetAllAsync();
        return Ok(courses);
    }

  
    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(int id)
    {
        var course = await _service.GetByIdAsync(id);
        return course == null
            ? NotFound(new { message = "Course not found." })
            : Ok(course);
    }

  
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateCourseDto dto)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        var created = await _service.CreateAsync(dto);
        return CreatedAtAction(nameof(GetById),
            new { id = created.CourseId }, created);
    }

  
    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, [FromBody] UpdateCourseDto dto)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        var updated = await _service.UpdateAsync(id, dto);
        return updated == null
            ? NotFound(new { message = "Course not found." })
            : Ok(updated);
    }


    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var deleted = await _service.DeleteAsync(id);
        return deleted
            ? NoContent()
            : NotFound(new { message = "Course not found." });
    }


    [HttpGet("{courseId}/lessons")]
    public async Task<IActionResult> GetLessons(int courseId)
    {
        var lessons = await _lessonService.GetByCourseIdAsync(courseId);
        return Ok(lessons);
    }
}