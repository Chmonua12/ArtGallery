using Microsoft.EntityFrameworkCore;
using ArtGallery.Domain.Entities;
using System.Reflection;

namespace ArtGallery.Infrastructure.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) 
            : base(options)
        {
        }

        public DbSet<Artist> Artists { get; set; }
        public DbSet<Museum> Museums { get; set; }
        public DbSet<Painting> Paintings { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            
            // Конфигурация через Fluent API
            modelBuilder.Entity<Artist>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.FirstName).IsRequired().HasMaxLength(100);
                entity.Property(e => e.LastName).IsRequired().HasMaxLength(100);
                entity.Property(e => e.Country).HasMaxLength(100);
                entity.Property(e => e.Biography).HasColumnType("ntext");
                
                entity.HasMany(a => a.Paintings)
                    .WithOne(p => p.Artist)
                    .HasForeignKey(p => p.ArtistId)
                    .OnDelete(DeleteBehavior.Cascade);
            });

            modelBuilder.Entity<Museum>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Name).IsRequired().HasMaxLength(200);
                entity.Property(e => e.City).HasMaxLength(100);
                entity.Property(e => e.Country).HasMaxLength(100);
                entity.Property(e => e.Description).HasColumnType("ntext");
            });

            modelBuilder.Entity<Painting>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Title).IsRequired().HasMaxLength(200);
                entity.Property(e => e.Dimensions).HasMaxLength(50);
                entity.Property(e => e.Description).HasColumnType("ntext");
                entity.Property(e => e.EstimatedValue).HasColumnType("decimal(18,2)");
                
                entity.HasOne(p => p.Museum)
                    .WithMany(m => m.Paintings)
                    .HasForeignKey(p => p.MuseumId)
                    .OnDelete(DeleteBehavior.SetNull);
            });
            
            // Применяем все конфигурации из текущей сборки
            modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
        }
    }
}