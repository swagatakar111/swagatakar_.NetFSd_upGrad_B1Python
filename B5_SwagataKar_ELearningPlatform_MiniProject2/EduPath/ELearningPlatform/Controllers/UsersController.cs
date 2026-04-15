using Microsoft.AspNetCore.Mvc;
using ELearningPlatform.DTOs;
using ELearningPlatform.Services.Interfaces;

namespace ELearningPlatform.Controllers;

[ApiController]
[Route("api/users")]
public class UsersController : ControllerBase
{
    private readonly IUserService _service;
    public UsersController(IUserService service) => _service = service;

    [HttpPost("register")]
    public async Task<IActionResult> Register([FromBody] RegisterUserDto dto)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        try
        {
            var user = await _service.RegisterAsync(dto);
            return CreatedAtAction(nameof(GetById),
                new { id = user.UserId }, user);
        }
        catch (InvalidOperationException ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }


    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(int id)
    {
        var user = await _service.GetByIdAsync(id);
        return user == null
            ? NotFound(new { message = "User not found." })
            : Ok(user);
    }


    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, [FromBody] UpdateUserDto dto)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        var updated = await _service.UpdateAsync(id, dto);
        return updated == null
            ? NotFound(new { message = "User not found." })
            : Ok(updated);
    }

    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginUserDto dto)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState);

        var user = await _service.LoginAsync(dto.Email, dto.Password);
        return user == null
            ? Unauthorized(new { message = "Invalid email or password." })
            : Ok(user);
    }
}