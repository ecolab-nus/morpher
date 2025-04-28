// Simulation precision
`timescale 1 ns / 1 ps

`define TB_NUM_INST 36357
`define TB_NUM_DMEM_INST 32768
`define TB_NUM_CMEM_INST 3584

`include "tb_defines.vh"
`include "globals_top.vh"
`include "uvm_macros.svh"
`include "qspi_rw_task.svh"
`include "pace_rw_task.svh"
`include "tb_driver.svh"

module tb_top();

//------------------------------------------------------------------------------
// Module instantiation
//------------------------------------------------------------------------------

//Common testbench driver module
tb_driver tb_driver();

//SoC DUT
`INSTANTIATE_DUT

//------------------------------------------------------------------------------
// Simulation signals / registers
//------------------------------------------------------------------------------
logic [`QSPI_DATA_WIDTH-1:0] val1, val2;
integer num_sim_cycles = `TB_NUM_SIM_CYCLES;
event initial_signals;
event start_stimulus;
bit marker_reg = 0;

// Used to view expected results (results_expected.trc) in waveform
wire [15:0] dmem_expected;
assign dmem_expected = memory_dataSRAM_expected[num_inst];

//------------------------------------------------------------------------------
// Initial values
//------------------------------------------------------------------------------
initial begin: initial_signals_block
    @ (initial_signals);
        scan_data_or_addr = 1'b0;
        read_write = 1'b0;
        scan_start_exec = 1'b0;
        //bist_en = 1'b0;
        // spi_en = 1'b0;
        //scan_data = 16'b0000000000000000;
        // clkSel = 6'd0;
        // divSel = 4'd0;
        // fixdivSel = 2'd0;
        // clkEn = 1'b0;
        // vcoEn = 1'b0;
        // clkExtEn = 1'b0;
end

//------------------------------------------------------------------------------
// Simulation control flow
//------------------------------------------------------------------------------
initial begin: simulation_control_flow
    initialize_testbench("$REPO_ROOT/verif/conv1x1/totaldata.trc",
                         "$REPO_ROOT/verif/conv1x1/totaladdr.trc",
                         "$REPO_ROOT/verif/conv1x1/results_expected.trc");
    //$set_toggle_region(hycube8x8_app_testbench.testbench_dut);

//vishnup TODO: Temp force, replace with global tasks
`ifdef QSPI_TEST_ENABLE
    force `SOC_TOP.hycube0.scan_start_exec = scan_start_exec;
    force exec_end = `SOC_TOP.hycube0.exec_end;
`else
    force `SOC_TOP.hycube0.data_in = data_in;
    force `SOC_TOP.hycube0.address_in = address_in;
    force `SOC_TOP.hycube0.data_addr_valid = data_addr_valid;
    force `SOC_TOP.hycube0.scan_start_exec = scan_start_exec;
    force `SOC_TOP.hycube0.read_write = read_write;
    force data_out_valid = `SOC_TOP.hycube0.data_out_valid;
    force data_out = `SOC_TOP.hycube0.data_out;
    force exec_end = `SOC_TOP.hycube0.exec_end;
`endif

    -> initial_signals;

    wait (tb_driver.rst_seq_done); //Wait for reset sequence to complete

    // Enable hycube chip (reset, chip_en)
    #(`SYS_CLK_PERIOD*10);
    qspi_unlock(`QSPI_PACE_ID, 12); // Unlock QSPI ctrl
    qspi_write(20'h80000, 16'h0110); // Enable hycube (reg0)

    // Print instance
    #(`SYS_CLK_PERIOD*10);
    $display("TB_NUM_INST: %d\n", `TB_NUM_INST);

    // LOAD SRAM (CMEM and DMEM)
    #(`SYS_CLK_PERIOD*10);
    for(num_inst=0; num_inst < `TB_NUM_INST; num_inst++) begin
        load_SRAM;
    end
    $display("[%16d] Stage : MEM load completed\n", $realtime);

    // CHECK DATA SRAM
    #(`SYS_CLK_PERIOD*10);
    $display("[%16d] Stage : Checking DMEM....\n", $realtime);
    for(num_inst=0; num_inst < `TB_NUM_DMEM_INST; num_inst++) begin
        check_dataSRAM;
    end

    // LOAD CONFIG
    //#(`SYS_CLK_PERIOD*10);
    //for(num_inst= `TB_NUM_CMEM_INST+`TB_NUM_DMEM_INST; num_inst < `TB_NUM_INST; num_inst++) begin
    //    load_SRAM;
    //end
    //$display("[%16d] Stage : CONFIG load completed\n", $realtime);

    #(`SYS_CLK_PERIOD*10);
    scan_start_exec = 1'b1;
    $display("[%16d] ASK : START EXEC\n", $realtime);

    @(posedge exec_end);
    $display("[%16d] ASK : END EXEC\n", $realtime);
    #(`SYS_CLK_PERIOD*50);
    scan_start_exec = 1'b0;

    // VERIFY RESULTING SRAM
    $display("[%16d] Stage : Verifying DMEM....\n", $realtime);
    for(num_inst=0; num_inst < `TB_NUM_DMEM_INST; num_inst++) begin
        verify_dataSRAM;
    end

    if(success)
        $display("Test Success.\n");
    else
        $display("Test Failed.\n");

    $finish();
end

//TB timeout section
initial begin
    #0.1s
    $error("Error: Test timeout\n");
    $fatal;
end

endmodule
