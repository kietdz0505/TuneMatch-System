package com.music.tunematch.repository;

import com.music.tunematch.entity.Song;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;

public interface SongRepository extends JpaRepository<Song, Long> {

    @Query("SELECT s FROM Song s WHERE s.minFrequency >= :userMinHz AND s.maxFrequency <= :userMaxHz")
    List<Song> findSongsMatchingVocalRange(@Param("userMinHz") double userMinHz, @Param("userMaxHz") double userMaxHz);
}