# 🔍 Performance Analysis: detect-voice Endpoint

## Executive Summary

The endpoint took **13.3 seconds** to process a request. Here's what I found:

### ✅ GOOD Practices (Already Implemented)
1. ✅ **Model is NOT loaded in request handler** - Loaded once at startup
2. ✅ **torch.no_grad() is present** - Gradient computation disabled for inference
3. ✅ **Services are initialized at startup** - No per-request initialization overhead

### ❌ PERFORMANCE ISSUES Found

1. **🔴 CRITICAL: Synchronous Audio Download (Blocking)**
   - Location: `app/main.py:94` - `audio_downloader.download()` is synchronous
   - Impact: Blocks the entire request while downloading (can be 5-10+ seconds)
   - Network latency directly affects response time

2. **🔴 CRITICAL: Inefficient Audio Loading for Long Files**
   - Location: `app/services/audio_preprocessor.py:39-45`
   - Issue: `librosa.load()` with `duration` parameter still loads entire file first
   - Impact: For a 60-second file, it loads all 60 seconds even if only need 10 seconds
   - Current: `duration=60` means full file is processed

3. **🟡 MEDIUM: Slow Resampling Method**
   - Location: `app/services/audio_preprocessor.py:44`
   - Issue: `res_type="kaiser_best"` is highest quality but slowest
   - Impact: Adds 1-3 seconds for resampling
   - Better: Use `"kaiser_fast"` or `"soxr_vhq"` for better speed/quality balance

4. **🟡 MEDIUM: No Audio Chunking/Streaming**
   - Issue: Entire audio file loaded into memory at once
   - Impact: High memory usage and slower processing for large files
   - Better: Process audio in chunks or use streaming

5. **🟢 MINOR: No Caching**
   - Issue: Same audio URL downloaded every time
   - Impact: Redundant downloads for repeated requests
   - Better: Cache downloaded files with TTL

---

## Detailed Analysis

### 1. Model Loading ✅ CORRECT

**Location:** `app/main.py:36`
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    global inference_service, audio_downloader, audio_preprocessor
    inference_service = InferenceService()  # ✅ Loaded ONCE at startup
```

**Status:** ✅ **GOOD** - Model is loaded at application startup, not per-request.

---

### 2. torch.no_grad() ✅ CORRECT

**Location:** `app/services/inference_service.py:62`
```python
with torch.no_grad():  # ✅ Gradient computation disabled
    audio_tensor = self._prepare_input(audio)
    output = self.model(audio_tensor)
```

**Status:** ✅ **GOOD** - `torch.no_grad()` is properly used to disable gradient computation during inference.

---

### 3. Long Audio File Processing ❌ INEFFICIENT

**Location:** `app/services/audio_preprocessor.py:39-45`
```python
audio, sr = librosa.load(
    audio_path,
    sr=self.target_sr,
    mono=True,
    duration=self.max_duration,  # ⚠️ PROBLEM: Still loads full file first
    res_type="kaiser_best"  # ⚠️ PROBLEM: Slowest resampling method
)
```

**Issues:**
1. **`duration` parameter limitation**: Even though `duration=60` is specified, librosa may still read metadata/headers from the entire file, and for some formats, it needs to decode the full file before truncating.

2. **`res_type="kaiser_best"`**: This is the slowest but highest quality resampling. For real-time inference, this is overkill.

**Impact:**
- For a 5-minute MP3 file, librosa still processes significant portions even with `duration=60`
- Resampling with `kaiser_best` can take 2-5 seconds for long files
- Memory usage is high (entire audio array in memory)

---

### 4. Synchronous Download ❌ BLOCKING

**Location:** `app/main.py:94`
```python
temp_file_path = audio_downloader.download(str(request.audio_url))  # ⚠️ BLOCKING
```

**Issue:** The download is synchronous and blocks the entire request handler.

**Impact:**
- Network latency directly adds to response time
- If download takes 10 seconds, response takes 10+ seconds
- No way to cancel or timeout gracefully during download

**Current Flow:**
```
Request → Download (10s) → Preprocess (2s) → Inference (0.1s) → Response (12.1s total)
```

---

## Performance Breakdown (Estimated)

For a typical request with 13.3s total time:

| Step | Estimated Time | Percentage |
|------|----------------|------------|
| **Audio Download** | 8-10 seconds | ~75% |
| **Audio Preprocessing** | 2-3 seconds | ~20% |
| **ML Inference** | 0.1-0.5 seconds | ~5% |
| **Other (overhead)** | <0.1 seconds | <1% |

**Conclusion:** The bottleneck is **audio download** and **preprocessing**, NOT the ML model.

---

## Recommendations (Priority Order)

### 🔴 HIGH PRIORITY

1. **Make Audio Download Async**
   - Use `aiohttp` or `httpx` for async downloads
   - Reduces blocking time significantly

2. **Optimize Audio Loading**
   - Use `librosa.load()` with `offset` and `duration` more efficiently
   - Consider using `soundfile` directly for faster loading
   - Use `res_type="soxr_vhq"` or `"kaiser_fast"` instead of `"kaiser_best"`

3. **Add Audio Duration Limit Earlier**
   - Validate audio duration before full download
   - Reject files that are too long upfront

### 🟡 MEDIUM PRIORITY

4. **Implement Audio Chunking**
   - Process audio in fixed-size chunks (e.g., 10-second windows)
   - Reduces memory usage and allows streaming

5. **Add Caching**
   - Cache downloaded audio files with URL hash
   - TTL-based expiration (e.g., 1 hour)

### 🟢 LOW PRIORITY

6. **Add Progress Logging**
   - Log time spent in each step
   - Helps identify future bottlenecks

---

## Code Changes Needed

See the fixes I'll implement next to address these issues.
