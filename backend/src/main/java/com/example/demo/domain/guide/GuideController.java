package com.example.demo.domain.guide;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/guides")
@RequiredArgsConstructor
@CrossOrigin(origins = "*") // 테스트 편의를 위해 전체 허용
@Tag(name = "Guide API", description = "신입 온보딩 및 회고 가이드 관리 API")
public class GuideController {

    private final GuideService guideService;

    @GetMapping
    @Operation(summary = "가이드 목록 조회", description = "저장된 모든 가이드와 회고록 목록을 반환합니다.")
    public List<Guide> getAllGuides() {
        return guideService.getAllGuides();
    }

    @GetMapping("/{id}")
    @Operation(summary = "가이드 상세 조회", description = "ID를 통해 특정 가이드의 마크다운 내용을 조회합니다.")
    public Guide getGuide(@PathVariable Long id) {
        return guideService.getGuide(id);
    }

    @PostMapping("/sync")
    @Operation(summary = "가이드 동기화", description = "로컬 파일 시스템의 마크다운 파일을 DB와 동기화합니다.")
    public void sync() {
        guideService.syncGuides();
    }
}
