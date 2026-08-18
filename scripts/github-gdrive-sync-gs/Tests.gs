function Test_all() {
  Logger.log("");
  Logger.log("########################################");
  Logger.log("START RUNNING ALL TEST SUITES");
  Logger.log("########################################");

  // Reset TestRunner state before run
  TestRunner.results = [];
  TestRunner.warnings = [];

  // Run each suite
  TestRunner.startSuite("ValidationTest");
  ValidationTest_all();

  TestRunner.startSuite("PathUtilsTest");
  PathUtilsTest_all();

  TestRunner.startSuite("MainTest");
  MainTest_all();

  TestRunner.startSuite("GithubClientTest");
  GithubClientTest_all();

  TestRunner.startSuite("DriveClientTest");
  DriveClientTest_all();

  TestRunner.startSuite("SyncServiceTest");
  SyncServiceTest_all();

  // Print consolidated summary and throw if failed
  TestRunner.printSummary();
}
