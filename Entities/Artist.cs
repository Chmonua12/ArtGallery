// ArtGallery.Domain/Entities/Artist.cs
using System.Collections.Generic;
using ArtGallery.Domain.Common;

namespace ArtGallery.Domain.Entities
{
    public class Artist : BaseEntity
    {
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Biography { get; set; }
        public DateTime BirthDate { get; set; }
        public DateTime? DeathDate { get; set; }
        public string Country { get; set; }
        
        // Навигационные свойства
        public virtual ICollection<Painting> Paintings { get; set; }
        
        public Artist()
        {
            Paintings = new HashSet<Painting>();
        }
        
        public string FullName => $"{FirstName} {LastName}";
    }
}