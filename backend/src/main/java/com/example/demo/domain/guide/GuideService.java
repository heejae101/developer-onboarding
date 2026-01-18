package com.example.demo.domain.guide;

import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Stream;

@Service
@RequiredArgsConstructor
@Slf4j
public class GuideService {

    private final GuideRepository guideRepository;
    private final String GUIDE_PATH = "/Users/chaehuijae/Desktop/가이드";

    @PostConstruct
    public void init() {
        syncGuides();
    }

    @Transactional
    public void syncGuides() {
        log.info("Scanning guides from: {}", GUIDE_PATH);
        try (Stream<Path> paths = Files.walk(Paths.get(GUIDE_PATH), 1)) {
            paths.filter(Files::isRegularFile)
                    .filter(path -> path.toString().endsWith(".md"))
                    .forEach(this::saveOrUpdateGuide);
        } catch (IOException e) {
            log.error("Failed to scan guides", e);
        }
    }

    private void saveOrUpdateGuide(Path path) {
        String fileName = path.getFileName().toString();
        String title = fileName.replace(".md", "");
        try {
            String content = Files.readString(path);
            Guide guide = guideRepository.findByTitle(title)
                    .orElse(new Guide());

            guide.setTitle(title);
            guide.setContent(content);
            guide.setFilePath(path.toString());

            // 파일명이나 내용에 따라 카테고리 임시 할당 로직 (필요시 프론트에서 수정 가능하게 하거나 파일 경로별로 나눌 수 있음)
            if (title.contains("목표"))
                guide.setCategory("하루 목표");
            else if (title.contains("지도") || title.contains("OpenLayers"))
                guide.setCategory("지도 예시");
            else if (title.contains("질문"))
                guide.setCategory("스스로 질문");
            else
                guide.setCategory("개발 공부");

            guideRepository.save(guide);
            log.info("Synced guide: {} [{}]", title, guide.getCategory());
        } catch (IOException e) {
            log.error("Failed to read guide file: {}", path, e);
        }
    }

    public List<Guide> getAllGuides() {
        return guideRepository.findAll();
    }

    public Guide getGuide(Long id) {
        return guideRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Guide not found with id: " + id));
    }
}
