using ArtGallery.Application.DTOs;
using ArtGallery.Application.Interfaces;
using ArtGallery.Domain.Entities;
using AutoMapper;

namespace ArtGallery.Application.Services
{
    public class ArtistService : IArtistService
    {
        private readonly IArtistRepository _artistRepository;
        private readonly IMapper _mapper;

        public ArtistService(IArtistRepository artistRepository, IMapper mapper)
        {
            _artistRepository = artistRepository;
            _mapper = mapper;
        }

        public async Task<IEnumerable<ArtistDto>> GetAllArtistsAsync()
        {
            var artists = await _artistRepository.GetAllAsync();
            return _mapper.Map<IEnumerable<ArtistDto>>(artists);
        }

        public async Task<ArtistDto> GetArtistByIdAsync(int id)
        {
            var artist = await _artistRepository.GetByIdAsync(id);
            return _mapper.Map<ArtistDto>(artist);
        }

        public async Task<ArtistDto> CreateArtistAsync(CreateArtistDto createArtistDto)
        {
            var artist = _mapper.Map<Artist>(createArtistDto);
            var createdArtist = await _artistRepository.AddAsync(artist);
            return _mapper.Map<ArtistDto>(createdArtist);
        }

        public async Task UpdateArtistAsync(int id, CreateArtistDto updateArtistDto)
        {
            var artist = await _artistRepository.GetByIdAsync(id);
            if (artist == null)
                throw new KeyNotFoundException($"Artist with id {id} not found");

            _mapper.Map(updateArtistDto, artist);
            await _artistRepository.UpdateAsync(artist);
        }

        public async Task DeleteArtistAsync(int id)
        {
            var artist = await _artistRepository.GetByIdAsync(id);
            if (artist == null)
                throw new KeyNotFoundException($"Artist with id {id} not found");

            await _artistRepository.DeleteAsync(artist);
        }

        public async Task<IEnumerable<PaintingDto>> GetArtistPaintingsAsync(int artistId)
        {
            var artist = await _artistRepository.GetArtistWithPaintingsAsync(artistId);
            if (artist == null)
                throw new KeyNotFoundException($"Artist with id {artistId} not found");

            return _mapper.Map<IEnumerable<PaintingDto>>(artist.Paintings);
        }
    }
}