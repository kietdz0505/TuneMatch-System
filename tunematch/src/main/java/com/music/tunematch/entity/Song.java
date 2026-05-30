package com.music.tunematch.entity;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "songs")
@Data
public class Song {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    @Column(nullable = false)
    private String artist;

    @Column(name = "min_frequency")
    private double minFrequency;

    @Column(name = "max_frequency")
    private double maxFrequency;

    private String minNote;
    private String maxNote;
}