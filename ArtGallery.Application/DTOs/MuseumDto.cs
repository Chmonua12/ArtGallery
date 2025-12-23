
namespace ArtGallery.Application.DTOs
{
    public class MuseumDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Address { get; set; }
        public string City { get; set; }
        public string Country { get; set; }
        public string Description { get; set; }
        public DateTime FoundationDate { get; set; }
        public DateTime CreatedAt { get; set; }
    }
    
    public class CreateMuseumDto
    {
        public string Name { get; set; }
        public string Address { get; set; }
        public string City { get; set; }
        public string Country { get; set; }
        public string Description { get; set; }
        public DateTime FoundationDate { get; set; }
    }
}