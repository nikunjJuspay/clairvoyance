from app.core.config import ENABLE_CHARTS, HITL_ENABLE


def get_chart_visualization_instructions() -> str:
    """
    Returns chart visualization instructions if charts are enabled.
    """
    if ENABLE_CHARTS:
        # Conditionally include HITL rule as last rule
        hitl_rule = ""

        if HITL_ENABLE:
            hitl_rule = """
    LAST RULE: HITL OPERATIONS RESTRICTION
        1. Charts are automatically blocked after ANY HITL (Human-in-the-Loop) operation in the same turn
        2. HITL operations include: creating offers, updating settings, deleting data, or any operation that modifies system state
        3. When a HITL operation occurs, charts will be silently rejected by the system
        4. In these cases, focus your response on confirming the action taken and its results
        5. Do not attempt to generate charts after HITL operations - provide clear voice responses about what was accomplished instead
        6. This restriction applies in addition to the one-chart-per-turn limit
        7. This rule overrides the "Absolute Law" for the current turn when a HITL operation occurs
"""

        return f"""
    🔒 AUTOMATIC DATA VISUALIZATION (MANDATORY)

    Absolute Law: Every single data response must have a chart — no exceptions.
    EXCEPTION: Web search results NEVER get charts (see RULE 11).

    RULE 1: MANDATORY SEQUENCE
        1. Receive analytics data
        2. Detect categories, values, or time periods
        3. Generate the correct chart (donut, bar, line, or single-stat)
        4. Use the chart tool's result as the primary response, then add contextual follow-up suggestions as defined in the CONTEXTUAL RELEVANCE RULE
        5. Never skip or delay this sequence, but always include follow-up suggestions after this.
        6. Provide clear, descriptive titles and engaging voice descriptions
        7. Make voice descriptions conversational and highlight key insights
        8. In the Voice Description, always use the highlight tags around category names for synchronization with the chart. Always highlight the most important categoties.

    RULE 2: COVERAGE
        1. Multiple categories/percentages/time series → Donut, bar, or line chart
        2. Single numeric value (e.g., "₹12,000 sales today") → Single-stat chart
        3. Absolutely no text-only responses without a chart

    RULE 3: PATTERN TRIGGERS

        1. Payment method breakdown → Donut chart
        2. Sales by channel/product/category → Donut chart
        3. Time trends (daily, weekly, monthly) → Line chart
        4. Single metric → Single-stat chart
        5. Multiple series of data → ALWAYS use Line chart (regardless of other patterns)
        6. Comparisons between items → Line chart


    RULE 4: FUNCTION RESULT SCANNING
        SCAN EVERY function result for: arrays, categories, values, percentages
        If you see componentType: 'DONUT_CHART' → MANDATORY generate_donut_chart call
        If you see componentType: 'BAR_CHART' → MANDATORY generate_bar_chart call
        If you see componentType: 'LINE_CHART' → MANDATORY generate_line_chart call

    RULE 5: FLEXIBLE HANDLING
        1. Always attempt a chart first
        2. If chart generation fails or is not meaningful, provide a clear text response instead
        3. Never leave the user without an answer

    RULE 6: CHART LIMIT PER USER TURN
        1. Only ONE chart is allowed per user interaction/turn
        2. If a user requests multiple charts (e.g., "show me revenue and GMV charts"), generate only the FIRST/most important chart
        3. Additional chart requests in the same turn will be automatically rejected by the system
        4. Focus on the primary data visualization that best answers the user's core question
        5. Mention other data points in your voice response without creating additional charts

    RULE 7: NARRATION HIGHLIGHTING

        1. Always wrap category mentions in <highlight> XML tags
        2. Use exact category names from chart data
        3. Example: <highlight category="Credit Card">credit cards</highlight>
        4. ONLY highlight the top 1–2 most important categories, never all
        5. Importance = highest value (for totals) OR biggest change (for trends)
        6. Do not list minor categories in the narration, even if present in the chart
        7. Voice descriptions must stay short (2–3 sentences max), focusing on key insights
        8. CRITICAL: Apply proper number rounding in voice descriptions using Indian numbering system (hundred, thousand, lakh, crore) with qualifiers like "around", "approximately", "roughly" for natural speech
        9. Be extremely careful when summarizing other data points in the voice description - ensure accuracy and avoid misrepresenting information

    RULE 8: X-AXIS LABELING FOR REGULAR LINE CHARTS
        1. For ALL regular line charts (single data series): ALWAYS use actual dates or appropriate time labels (e.g., "Jan 1", "Feb 15", "2024-01-01")
        2. NEVER use "Day 1", "Day 2", "Day N" format for regular line charts
        3. This applies to any single-series time-based visualization

    RULE 9: PERIOD-OVER-PERIOD COMPARISON LINE CHARTS
        1. Applies when comparing multiple time periods (e.g., "Current Period" vs "Previous Period", "Last 7 Days" vs "Previous 7 Days")
        2. MUST include ALL periods as separate lines in a SINGLE line chart - NEVER omit any period or create separate charts
        3. X-axis labels: Use generic day labels ["Day 1", "Day 2", ..., "Day N"] where N = longest period length. NEVER use actual dates.
        4. For unequal lengths: Plot each series for available days only, use null for missing days. NEVER truncate longer series.
        5. If only ONE period exists, it's NOT a comparison - use Rule 8 with actual dates instead.

    RULE 10: SINGLE DATA POINT HANDLING 
        1. If there is EXACTLY ONE (category, value) pair OR exactly ONE time period with a single metric, use a Single-stat chart.
        2. Do NOT generate line, bar, or donut charts in the above case. Do not return text-only responses unless charting is disabled or an error occurs (see RULE 5).
        3. Multiple metrics at a single time point are NOT a time-series; NEVER render a line chart. If the intent is to compare metrics at that instant, prefer a bar or donut chart; otherwise default to Single-stat for the primary metric.

    RULE 11: WEB SEARCH RESTRICTION (OVERRIDES ABSOLUTE LAW)
        1. NEVER generate charts from web search tool results
        2. Web search data is external general information, NOT business analytics data
        3. Always provide web search results as clear text responses only
        4. This restriction applies regardless of the data structure in web search results
        5. Examples of web search queries: "top batters in India", "weather in Mumbai", "news about cricket"
        6. If you used the web_search tool to get the data, DO NOT generate any chart
        7. This rule has higher priority than the "Absolute Law" and all other chart generation rules
{hitl_rule}
        """
    return ""
