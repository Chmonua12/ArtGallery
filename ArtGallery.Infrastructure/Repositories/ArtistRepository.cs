
using ArtGallery.Application.Interfaces;
using ArtGallery.Domain.Entities;
using ArtGallery.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace ArtGallery.Infrastructure.Repositories
{
    public class ArtistRepository : BaseRepository<Artist>, IArtistRepository
    {
        public ArtistRepository(AppDbContext context) : base(context)
        {
        }

        public async Task<IEnumerable<Artist>> GetArtistsWithPaintingsAsync()
        {
            return await _context.Artists
                .Include(a => a.Paintings)
                .ThenInclude(p => p.Museum)
                .ToListAsync();
        }

        public async Task<Artist> GetArtistWithPaintingsAsync(int id)
        {
            return await _context.Artists
                .Include(a => a.Paintings)
                .ThenInclude(p => p.Museum)
                .FirstOrDefaultAsync(a => a.Id == id);
        }
    }
}