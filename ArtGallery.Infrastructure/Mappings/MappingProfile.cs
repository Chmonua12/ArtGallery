using ArtGallery.Application.DTOs;
using ArtGallery.Domain.Entities;
using AutoMapper;

namespace ArtGallery.Application.Mappings
{
    public class MappingProfile : Profile
    {
        public MappingProfile()
        {
            CreateMap<Artist, ArtistDto>()
                .ForMember(dest => dest.FullName, opt => 
                    opt.MapFrom(src => $"{src.FirstName} {src.LastName}"));

            CreateMap<CreateArtistDto, Artist>();

            CreateMap<Museum, MuseumDto>();
            CreateMap<CreateMuseumDto, Museum>();

            CreateMap<Painting, PaintingDto>()
                .ForMember(dest => dest.ArtistName, opt => 
                    opt.MapFrom(src => src.Artist != null ? src.Artist.FullName : "Неизвестный художник"))
                .ForMember(dest => dest.MuseumName, opt => 
                    opt.MapFrom(src => src.Museum != null ? src.Museum.Name : "Частная коллекция"))
                .ForMember(dest => dest.MediumName, opt => 
                    opt.MapFrom(src => src.Medium.ToString()));

            CreateMap<CreatePaintingDto, Painting>();
        }
    }
}