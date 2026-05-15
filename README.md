# Comparative Evaluation of Language Models

This project provides a comprehensive framework for evaluating and comparing language models using multiple evaluation methodologies: **Natural Language Inference (NLI)** and **Text Similarity Analysis**. The project benchmarks both open-source models (Gemma, Mistral, Phi, Qwen) and commercial models (ChatGPT, Gemini).

## 🎯 Project Overview

The project evaluates language models through two primary approaches:

1. **Natural Language Inference (NLI)** - Assesses model understanding of textual relationships
2. **Similarity-Based Evaluation** - Measures text pair similarity with optimal threshold tuning

The framework includes:
- Ground truth datasets in multiple sizes (100 and 300 samples)
- Comparative analysis across open and closed-source models
- Threshold optimization using cross-validation
- Comprehensive metrics (Accuracy, F1-Score, Cohen's Kappa)

## 📁 Project Structure

```
├── data/
│   ├── 100_GT.csv                 # 100-sample ground truth dataset
│   ├── 300_GT.csv                 # 300-sample ground truth dataset
│   └── dataset/                   # Additional datasets
│
├── evaluation/
│   ├── nli_evaluation.py          # NLI evaluation script
│   ├── similarity.py              # Similarity-based evaluation
│   └── nli_evaluation.ipynb       # NLI notebook interface
│
├── notebooks/
│   ├── similarity.ipynb                         # Similarity analysis
│   ├── small_models.ipynb                       # Small model benchmarking
│   ├── chatgpt_gemini_single_prompt.ipynb      # Commercial model comparison
│   └── results/visualization.ipynb              # Result visualization
│
├── results/
│   ├── nli/                       # NLI evaluation results
│   ├── similarity/                # Similarity threshold analysis
│   ├── closed_models/             # ChatGPT/commercial model results
│   └── open_models/               # Open-source model results
│
└── LICENSE
```

## 🚀 Quick Start

### Prerequisites

```bash
pip install pandas scikit-learn sentence-transformers torch
```

### Running Similarity Evaluation

```bash
python similarity.py
```

This script:
- Loads ground truth data from CSV
- Computes TF-IDF cosine similarity for text pairs
- Performs threshold grid search (0.01 steps)
- Generates accuracy metrics

**Input CSV Format:**
```
APP Features 1 | Review 1 | APP Features 2 | Review 2 | Annotation
```

### Running NLI Evaluation

#### Without LLM Judge:
```bash
python nli_evaluation.py \
  --csv "100_GT.csv" \
  --model roberta-large-mnli \
  --target-label consensus_only \
  --objective kappa \
  --cv-folds 5 \
  --similarity-method cosine \
  --embedding-model sentence-transformers/all-MiniLM-L6-v2 \
  --nli-score-mode contra_norm
```

#### With GPT-5 API Judge:
```bash
python nli_evaluation.py \
  --csv "100_GT.csv" \
  --model MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli \
  --target-label consensus_only \
  --objective kappa \
  --cv-folds 5 \
  --llm-judge --llm-gpt5-api --llm-model gpt-5
```

## 📊 Evaluation Methods

### Similarity-Based Approach
- **Method**: TF-IDF Vectorization + Cosine Similarity
- **Threshold Tuning**: Grid search with step size 0.01
- **Metrics**: Accuracy, F1-Score, Cohen's Kappa
- **Output**: Optimal thresholds and confusion matrices

### NLI-Based Approach
- **Models Supported**: 
  - `roberta-large-mnli`
  - `DeBERTa-v3-base-mnli-fever-anli` (Recommended)
  - Custom NLI models
- **Scoring Modes**: Contradiction normalization
- **Validation**: 5-fold cross-validation
- **Optional**: LLM judge (GPT-5 API integration)

## 📈 Results

### Open-Source Models
- **Gemma2**: Metrics available in `results/open_models/gemma2_metrics_from_prompt_column.csv`
- **Mistral3**: Results in `results/open_models/ministral3_metrics_summary.csv`
- **Phi**: Metrics in `results/open_models/phi_llama_metrics.txt`
- **Qwen**: Results in `results/open_models/qwen_metrics.txt`

### Closed-Source Models
- **ChatGPT**: Analysis in `results/closed_models/100_sample_1_prompt_experiment_metrics.csv`
- **Gemini**: Comparative results in `nli_comparision/`

### Similarity Analysis
- **Threshold Results**: `results/similarity/threshold_search_results_*.csv`
- **Best Thresholds**: `results/similarity/best_thresholds_by_accuracy_*.csv`
- **Accuracy Path**: `results/similarity/accuracy_path_to_best_*.csv`

## 🔧 Usage Examples

### Jupyter Notebooks

1. **Similarity Analysis**
   ```bash
   jupyter notebook similarity.ipynb
   ```
   - Interactive threshold tuning
   - Visual threshold-accuracy curves
   - Model comparison dashboard

2. **NLI Evaluation**
   ```bash
   jupyter notebook nli_evaluation.ipynb
   ```
   - NLI model benchmarking
   - Cross-validation results
   - Confidence analysis

3. **Model Comparison**
   ```bash
   jupyter notebook chatgpt_gemini_single_prompt.ipynb
   ```
   - Side-by-side open vs. closed model comparison
   - Performance metrics visualization

## 📝 Dataset Format

Ground truth CSV files should contain:

| Column | Type | Description |
|--------|------|-------------|
| APP Features 1 | string | Features of first app/item |
| Review 1 | string | Review/description of first item |
| APP Features 2 | string | Features of second app/item |
| Review 2 | string | Review/description of second item |
| Annotation | int | 1=Same/Grouped, 0=Different/Separate |

## 🎛️ Configuration

### Similarity Evaluation Parameters
- `THRESHOLD_GRID_STEP`: Threshold step size (default: 0.01)
- `INPUT_CSV`: Input ground truth file
- `OUTPUT_CSV`: Output results file

### NLI Evaluation Parameters
- `--model`: HuggingFace NLI model identifier
- `--cv-folds`: Number of cross-validation folds (default: 5)
- `--objective`: Optimization metric (kappa, accuracy, f1)
- `--similarity-method`: cosine, euclidean, etc.

## 📊 Key Metrics

- **Accuracy**: Correctly classified pairs / Total pairs
- **F1-Score**: Harmonic mean of precision and recall
- **Cohen's Kappa**: Inter-rater agreement measure
- **Confusion Matrix**: True Positives, False Positives, True Negatives, False Negatives

## 🔍 Files Reference

### Main Scripts
- `nli_evaluation.py` - Primary NLI evaluation script with LLM judge support
- `similarity.py` - Similarity-based evaluation with threshold optimization
- `creating_prompt.py` - Utility for prompt generation/conversion

### Analysis Notebooks
- `nli_evaluation.ipynb` - Interactive NLI analysis
- `similarity.ipynb` - Interactive similarity analysis and visualization
- `small_models.ipynb` - Benchmarking smaller models
- `chatgpt_gemini_single_prompt.ipynb` - Commercial model comparison

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report issues and bugs
- Suggest improvements
- Add new evaluation methodologies
- Extend model support

## 📧 Contact

For questions or collaboration inquiries, please open an issue in the repository.

---

**Last Updated**: 2026
