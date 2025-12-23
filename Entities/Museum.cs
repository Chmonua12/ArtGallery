// ArtGallery.Domain/Entities/Museum.cs
using System.Collections.Generic;
using ArtGallery.Domain.Common;

namespace ArtGallery.Domain.Entities
{
    public class Museum : BaseEntity
    {
        public string Name { get; set; }
        public string Address { get; set; }
        public string City { get; set; }
        public string Country { get; set; }
        public string Description { get; set; }
        public DateTime FoundationDate { get; set; }
        
        // Навигационные свойства
        public virtual ICollection<Painting> Paintings { get; set; }
        
        public Museum()
        {
            Paintings = new HashSet<Painting>();
        }
    }
}