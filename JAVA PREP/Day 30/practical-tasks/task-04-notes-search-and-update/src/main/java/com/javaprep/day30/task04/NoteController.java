package com.javaprep.day30.task04;

import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/notes")
public class NoteController {

    private final NoteService service;

    public NoteController(NoteService service) {
        this.service = service;
    }

    /**
     * GET /api/notes?contains=x&limit=n
     *  - contains: optional case-insensitive substring filter on text
     *  - limit: optional max number of items returned (>= 0)
     *  - header X-Total-Count = number of notes matching the filter BEFORE limiting
     */
    @GetMapping
    public ResponseEntity<List<Note>> search(@RequestParam(required = false) String contains,
                                             @RequestParam(required = false) Integer limit) {
        // TODO(Day30-task04): filter, count, limit; return 200 with the X-Total-Count header
        throw new UnsupportedOperationException("TODO(Day30-task04): filter, count, limit; return 200 with the X-Total-Count header");
    }

    /**
     * PUT /api/notes/{id} with JSON {"text": "..."}:
     *  - 200 + updated note
     *  - 404 if the note does not exist
     *  - 400 with JSON {"error": "text must not be blank"} if text is null/blank
     * (check validity BEFORE the lookup)
     */
    @PutMapping("/{id}")
    public ResponseEntity<?> update(@PathVariable long id, @RequestBody Map<String, String> body) {
        // TODO(Day30-task04): validate text (400 + error body), then update and answer 200 or 404
        throw new UnsupportedOperationException("TODO(Day30-task04): validate text (400 + error body), then update and answer 200 or 404");
    }
}
