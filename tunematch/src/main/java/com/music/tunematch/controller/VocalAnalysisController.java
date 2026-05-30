package com.music.tunematch.controller;
import com.music.tunematch.service.VocalAnalysisService;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import java.util.Map;

@RestController
@RequestMapping("/api/vocal")
@CrossOrigin(origins = "*")
public class VocalAnalysisController {

    private final VocalAnalysisService vocalAnalysisService;

    public VocalAnalysisController(VocalAnalysisService vocalAnalysisService) {
        this.vocalAnalysisService = vocalAnalysisService;
    }

    @PostMapping("/analyze-and-recommend")
    public ResponseEntity<Map<String, Object>> analyzeAndRecommend(@RequestParam("file") MultipartFile file) {
        try {
            Map<String, Object> result = vocalAnalysisService.processVocalAnalysis(file);
            result.put("status", "success");
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("status", "error", "message", e.getMessage()));
        }
    }
}