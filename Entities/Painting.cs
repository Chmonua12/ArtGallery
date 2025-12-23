// ArtGallery.Domain/Entities/Painting.cs
using ArtGallery.Domain.Common;
using ArtGallery.Domain.Enums;

namespace ArtGallery.Domain.Entities
{
    public class Painting : BaseEntity
    {
        public string Title { get; set; }
        public int YearCreated { get; set; }
        public PaintingMedium Medium { get; set; }
        public string Dimensions { get; set; } // "100x150 cm"
        public string Description { get; set; }
        public decimal? EstimatedValue { get; set; }
        
        // Внешние ключи
        public int ArtistId { get; set; }
        public int? MuseumId { get; set; } // Может быть null если картина в частной коллекции
        
        // Навигационные свойства
        public virtual Artist Artist { get; set; }
        public virtual Museum Museum { get; set; }
    }
}