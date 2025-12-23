
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ArtGallery.Infrastructure.Data;
using ArtGallery.Domain.Entities;
using ArtGallery.Application.DTOs;

namespace ArtGallery.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PaintingsController : ControllerBase
    {
        private readonly AppDbContext _context;

        public PaintingsController(AppDbContext context)
        {
            _context = context;
        }

        // GET: api/Paintings
        [HttpGet]
        public async Task<ActionResult<IEnumerable<PaintingDto>>> GetPaintings()
        {
            var paintings = await _context.Paintings
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

        // GET: api/Paintings/5
        [HttpGet("{id}")]
        public async Task<ActionResult<PaintingDto>> GetPainting(int id)
        {
            var painting = await _context.Paintings
                .Include(p => p.Artist)
                .Include(p => p.Museum)
                .Where(p => p.Id == id)
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
                .FirstOrDefaultAsync();

            if (painting == null)
            {
                return NotFound();
            }

            return Ok(painting);
        }

        // POST: api/Paintings
        [HttpPost]
        public async Task<ActionResult<PaintingDto>> CreatePainting(CreatePaintingDto createPaintingDto)
        {
            // Проверяем существование художника
            var artist = await _context.Artists.FindAsync(createPaintingDto.ArtistId);
            if (artist == null)
            {
                return BadRequest("Artist not found");
            }

            // Проверяем существование музея (если указан)
            if (createPaintingDto.MuseumId.HasValue)
            {
                var museum = await _context.Museums.FindAsync(createPaintingDto.MuseumId.Value);
                if (museum == null)
                {
                    return BadRequest("Museum not found");
                }
            }

            var painting = new Painting
            {
                Title = createPaintingDto.Title,
                YearCreated = createPaintingDto.YearCreated,
                Medium = createPaintingDto.Medium,
                Dimensions = createPaintingDto.Dimensions,
                Description = createPaintingDto.Description,
                EstimatedValue = createPaintingDto.EstimatedValue,
                ArtistId = createPaintingDto.ArtistId,
                MuseumId = createPaintingDto.MuseumId,
                CreatedAt = DateTime.UtcNow
            };

            _context.Paintings.Add(painting);
            await _context.SaveChangesAsync();

            // Загружаем связанные данные для DTO
            await _context.Entry(painting)
                .Reference(p => p.Artist)
                .LoadAsync();

            await _context.Entry(painting)
                .Reference(p => p.Museum)
                .LoadAsync();

            var paintingDto = new PaintingDto
            {
                Id = painting.Id,
                Title = painting.Title,
                YearCreated = painting.YearCreated,
                Medium = painting.Medium,
                Dimensions = painting.Dimensions,
                Description = painting.Description,
                EstimatedValue = painting.EstimatedValue,
                ArtistId = painting.ArtistId,
                ArtistName = painting.Artist.FullName,
                MuseumId = painting.MuseumId,
                MuseumName = painting.Museum != null ? painting.Museum.Name : "Частная коллекция",
                CreatedAt = painting.CreatedAt
            };

            return CreatedAtAction(nameof(GetPainting), new { id = painting.Id }, paintingDto);
        }

        // PUT: api/Paintings/5
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdatePainting(int id, CreatePaintingDto updatePaintingDto)
        {
            var painting = await _context.Paintings.FindAsync(id);
            if (painting == null)
            {
                return NotFound();
            }

            // Проверяем существование художника
            var artist = await _context.Artists.FindAsync(updatePaintingDto.ArtistId);
            if (artist == null)
            {
                return BadRequest("Artist not found");
            }

            // Проверяем существование музея (если указан)
            if (updatePaintingDto.MuseumId.HasValue)
            {
                var museum = await _context.Museums.FindAsync(updatePaintingDto.MuseumId.Value);
                if (museum == null)
                {
                    return BadRequest("Museum not found");
                }
            }

            painting.Title = updatePaintingDto.Title;
            painting.YearCreated = updatePaintingDto.YearCreated;
            painting.Medium = updatePaintingDto.Medium;
            painting.Dimensions = updatePaintingDto.Dimensions;
            painting.Description = updatePaintingDto.Description;
            painting.EstimatedValue = updatePaintingDto.EstimatedValue;
            painting.ArtistId = updatePaintingDto.ArtistId;
            painting.MuseumId = updatePaintingDto.MuseumId;
            painting.UpdatedAt = DateTime.UtcNow;

            _context.Entry(painting).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!PaintingExists(id))
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

        // DELETE: api/Paintings/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeletePainting(int id)
        {
            var painting = await _context.Paintings.FindAsync(id);
            if (painting == null)
            {
                return NotFound();
            }

            _context.Paintings.Remove(painting);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool PaintingExists(int id)
        {
            return _context.Paintings.Any(e => e.Id == id);
        }

        // GET: api/Paintings/search?title=мона
        [HttpGet("search")]
        public async Task<ActionResult<IEnumerable<PaintingDto>>> SearchPaintings(
            [FromQuery] string title = null,
            [FromQuery] int? artistId = null,
            [FromQuery] int? museumId = null,
            [FromQuery] int? minYear = null,
            [FromQuery] int? maxYear = null)
        {
            var query = _context.Paintings
                .Include(p => p.Artist)
                .Include(p => p.Museum)
                .AsQueryable();

            if (!string.IsNullOrEmpty(title))
            {
                query = query.Where(p => p.Title.Contains(title));
            }

            if (artistId.HasValue)
            {
                query = query.Where(p => p.ArtistId == artistId.Value);
            }

            if (museumId.HasValue)
            {
                query = query.Where(p => p.MuseumId == museumId.Value);
            }

            if (minYear.HasValue)
            {
                query = query.Where(p => p.YearCreated >= minYear.Value);
            }

            if (maxYear.HasValue)
            {
                query = query.Where(p => p.YearCreated <= maxYear.Value);
            }

            var paintings = await query
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