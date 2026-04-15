using Microsoft.AspNetCore.Mvc;
using ELearningPlatform.Services.Interfaces;

namespace ELearningPlatform.Controllers;

[ApiController]
[Route("api/results")]
public class ResultsController : ControllerBase
{
    private readonly IQuizService _service;
    public ResultsController(IQuizService service) => _service = service;

  
    [HttpGet("{userId}")]
    public async Task<IActionResult> GetByUser(int userId)
    {
        var results = await _service.GetResultsByUserAsync(userId);
        return Ok(results);
    }
}