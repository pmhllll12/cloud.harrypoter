INTENT_MAP: dict[str, set[str]] = {
    "SURVIVAL_PREDICT": {
        "생존", "탈락", "살아남", "탈락했", "예측", "예상", "확률", "통과", "클리어",
        "survive", "survived", "eliminated", "predict", "probability", "clear",
    },
    "STATISTICS": {
        "몇", "명", "비율", "평균", "통계", "분포", "총", "전체", "합계",
        "count", "total", "average", "mean", "ratio", "percent", "statistics",
    },
    "CHAMPION_SEARCH": {
        "챔피언", "이름", "누구", "찾", "검색", "참가", "인물",
        "champion", "name", "who", "find", "search",
    },
    "MODEL_TRAIN": {
        "훈련", "학습", "모델", "알고리즘", "정확도", "성능", "테스트", "리트머스",
        "train", "training", "model", "algorithm", "accuracy", "fit", "test",
    },
}
