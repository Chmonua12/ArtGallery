
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ArtGallery.Infrastructure.Data;
using ArtGallery.Domain.Entities;
using ArtGallery.Application.DTOs;

namespace ArtGallery.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class MuseumsController : ControllerBase
    {
        private readonly AppDbContext _context;

        public MuseumsController(AppDbContext context)
        {
            _context = context;
        }

        // GET: api/Museums
        [HttpGet]
        public async Task<ActionResult<IEnumerable<MuseumDto>>> GetMuseums()
        {
            var museums = await _context.Museums
                .Select(m => new MuseumDto
                {
                    Id = m.Id,
                    Name = m.Name,
                    Address = m.Address,
                    City = m.City,
                    Country = m.Country,
                    Description = m.Description,
                    FoundationDate = m.FoundationDate,
                    CreatedAt = m.CreatedAt
                })
                .ToListAsync();

            return Ok(museums);
        }

        // GET: api/Museums/5
        [HttpGet("{id}")]
        public async Task<ActionResult<MuseumDto>> GetMuseum(int id)
        {
            var museum = await _context.Museums
                .Where(m => m.Id == id)
                .Select(m => new MuseumDto
                {
                    Id = m.Id,
                    Name = m.Name,
                    Address = m.Address,
                    City = m.City,
                    Country = m.Country,
                    Description = m.Description,
                    FoundationDate = m.FoundationDate,
                    CreatedAt = m.CreatedAt
                })
                .FirstOrDefaultAsync();

            if (museum == null)
            {
                return NotFound();
            }

            return Ok(museum);
        }

        // POST: api/Museums
        [HttpPost]
        public async Task<ActionResult<MuseumDto>> CreateMuseum(CreateMuseumDto createMuseumDto)
        {
            var museum = new Museum
            {
                Name = createMuseumDto.Name,
                Address = createMuseumDto.Address,
                City = createMuseumDto.City,
                Country = createMuseumDto.Country,
                Description = createMuseumDto.Description,
                FoundationDate = createMuseumDto.FoundationDate,
                CreatedAt = DateTime.UtcNow
            };

            _context.Museums.Add(museum);
            await _context.SaveChangesAsync();

            var museumDto = new MuseumDto
            {
                Id = museum.Id,
                Name = museum.Name,
                Address = museum.Address,
                City = museum.City,
                Country = museum.Country,
                Description = museum.Description,
                FoundationDate = museum.FoundationDate,
                CreatedAt = museum.CreatedAt
            };

            return CreatedAtAction(nameof(GetMuseum), new { id = museum.Id }, museumDto);
        }

        // PUT: api/Museums/5
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateMuseum(int id, CreateMuseumDto updateMuseumDto)
        {
            var museum = await _context.Museums.FindAsync(id);
            if (museum == null)
            {
                return NotFound();
            }

            museum.Name = updateMuseumDto.Name;
            museum.Address = updateMuseumDto.Address;
            museum.City = updateMuseumDto.City;
            museum.Country = updateMuseumDto.Country;
            museum.Description = updateMuseumDto.Description;
            museum.FoundationDate = updateMuseumDto.FoundationDate;
            museum.UpdatedAt = DateTime.UtcNow;

            _context.Entry(museum).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!MuseumExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // DELETE: api/Museums/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteMuseum(int id)
        {
            var museum = await _context.Museums.FindAsync(id);
            if (museum == null)
            {
                return NotFound();
            }

            _context.Museums.Remove(museum);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool MuseumExists(int id)
        {
            return _context.Museums.Any(e => e.Id == id);
        }

        // GET: api/Museums/5/Paintings
        [HttpGet("{id}/paintings")]
        public async Task<ActionResult<IEnumerable<PaintingDto>>> GetMuseumPaintings(int id)
        {
            var paintings = await _context.Paintings
                .Where(p => p.MuseumId == id)
                .Include(p => p.Artist)
                .Include(p => p.Museum)
                .Select(p => new PaintingDto
                {
                    Id = p.Id,
                    Title = p.Title,
                    YearCreated = p.YearCreated,
                    Medium = p.Medium,
                    Dimensions = p.Dimensions,
                    Description = p.Description,
                    EstimatedValue = p.EstimatedValue,
                    ArtistId = p.ArtistId,
                    ArtistName = p.Artist.FullName,
                    MuseumId = p.MuseumId,
                    MuseumName = p.Museum != null ? p.Museum.Name : "Частная коллекция",
                    CreatedAt = p.CreatedAt
                })
                .ToListAsync();

            return Ok(paintings);
        }
    }
}