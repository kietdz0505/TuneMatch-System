package com.music.tunematch.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.music.tunematch.entity.Song;
import com.music.tunematch.repository.SongRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class VocalAnalysisService {

    @Value("${python.api.url}")
    private String pythonApiUrl;

    private final SongRepository songRepository;
    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    public VocalAnalysisService(SongRepository songRepository) {
        this.songRepository = songRepository;
        this.restTemplate = new RestTemplate();
        this.objectMapper = new ObjectMapper();
    }

    public Map<String, Object> processVocalAnalysis(MultipartFile file) throws Exception {
        File tempFile = File.createTempFile("vocal_", file.getOriginalFilename());
        file.transferTo(tempFile);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", new FileSystemResource(tempFile));

        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
        ResponseEntity<String> pythonResponse = restTemplate.postForEntity(pythonApiUrl, requestEntity, String.class);
        tempFile.delete();

        JsonNode rootNode = objectMapper.readTree(pythonResponse.getBody());
        if (!"success".equals(rootNode.path("status").asText())) {
            throw new RuntimeException("Python service không phân tích được âm thanh.");
        }

        JsonNode dataNode = rootNode.get("data");
        double minHz = dataNode.get("min_frequency_hz").asDouble();
        double maxHz = dataNode.get("max_frequency_hz").asDouble();
        String minNote = dataNode.get("min_note").asText();
        String maxNote = dataNode.get("max_note").asText();

        List<Song> recommendedSongs = songRepository.findSongsMatchingVocalRange(minHz, maxHz);

        Map<String, Object> result = new HashMap<>();
        result.put("user_vocal_range", Map.of(
                "min_note", minNote, "max_note", maxNote,
                "min_hz", minHz, "max_hz", maxHz
        ));
        result.put("recommended_songs", recommendedSongs);
        return result;
    }
}