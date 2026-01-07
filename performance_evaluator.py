class PerformanceEvaluator:
    @staticmethod
    def print_summary_table(stats_list):
        print("\n" + "="*75)
        print("                  FINAL PERFORMANCE SUMMARY")
        print("="*75)
        print(
            f"{'Scenario':<25} | {'Status':<10} | {'Time':<10} | {'Length':<12} | {'Steps':<8}")
        print("-" * 75)

        for stat in stats_list:
            status = "SUCCESS" if stat.success else "FAILED"
            print(f"{stat.scenario_name:<25} | {status:<10} | {stat.planning_time_ms:<6} ms | {stat.path_length:<12.2f} | {stat.num_steps:<8}")
        print("="*75)
