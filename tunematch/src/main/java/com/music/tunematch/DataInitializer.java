package com.music.tunematch;

import com.music.tunematch.entity.Song;
import com.music.tunematch.repository.SongRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {

    private final SongRepository songRepository;

    public DataInitializer(SongRepository songRepository) {
        this.songRepository = songRepository;
    }

    @Override
    public void run(String... args) throws Exception {

    }
}